"""
Smart Grocery Budget Planner - Local Web Application Server
============================================================
Lightweight HTTP & REST API server built with Python's standard library `http.server`.
Requires NO external packages (no Flask, no FastAPI needed).

Serves:
- Static Web Frontend (index.html, style.css, app.js)
- REST API for live synchronization with grocery_data.json via DataManager & GroceryManager

Usage:
    python server.py
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from grocery_manager import GroceryManager
from data_manager import DataManager

# Cloud / Render deployment configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 5000))

# Shared manager singletons
dm = DataManager()
loaded_data, _ = dm.load_data()
gm = GroceryManager()
gm.load_from_dict(loaded_data)


class GroceryApiHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler combining static web file serving
    and JSON REST API endpoints.
    """

    def _send_json_response(self, data, status_code=200):
        """Helper to serialize and transmit JSON responses."""
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Route GET requests to API or static assets."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path in ("/healthz", "/api/health"):
            self._send_json_response({"status": "healthy", "service": "smart-grocery-budget-planner"})
            return

        if path == "/api/data":
            # Return complete current state
            status = gm.get_budget_status()
            cat_stats = gm.get_category_spending()
            suggestions = gm.get_smart_suggestions()

            self._send_json_response({
                "budget": gm.get_budget(),
                "items": gm.get_all_items(),
                "total_spent": gm.get_total_spent(),
                "remaining": gm.get_remaining_budget(),
                "percentage_used": gm.get_budget_percentage(),
                "status": status,
                "category_breakdown": cat_stats,
                "suggestions": suggestions
            })
            return

        # Default: Serve static files from workspace directory
        if path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        """Route POST requests for data mutation."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            body = json.loads(post_body) if post_body else {}
        except json.JSONDecodeError:
            self._send_json_response({"error": "Invalid JSON body"}, 400)
            return

        if path == "/api/budget":
            budget_val = body.get("budget")
            success, msg = gm.set_budget(budget_val)
            if success:
                dm.save_data(gm.get_budget(), gm.get_all_items())
                self._send_json_response({"success": True, "message": msg, "budget": gm.get_budget()})
            else:
                self._send_json_response({"success": False, "error": msg}, 400)
            return

        elif path == "/api/items":
            name = body.get("name")
            category = body.get("category", "Other")
            quantity = body.get("quantity", 1)
            price = body.get("price_per_unit", 0)
            unit = body.get("unit", "units")

            success, msg, item = gm.add_item(name, category, quantity, price, unit)
            if success:
                dm.save_data(gm.get_budget(), gm.get_all_items())
                self._send_json_response({"success": True, "message": msg, "item": item})
            else:
                self._send_json_response({"success": False, "error": msg}, 400)
            return

        elif path == "/api/save":
            success, msg = dm.save_data(gm.get_budget(), gm.get_all_items())
            self._send_json_response({"success": success, "message": msg})
            return

        elif path == "/api/reset":
            data, msg = dm.reset_to_defaults()
            gm.load_from_dict(data)
            self._send_json_response({
                "success": True,
                "message": msg,
                "budget": gm.get_budget(),
                "items": gm.get_all_items()
            })
            return

        self._send_json_response({"error": f"Endpoint '{path}' not found"}, 404)

    def do_PUT(self):
        """Route PUT requests for item modification."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path.startswith("/api/items/"):
            try:
                item_id = int(path.split("/")[-1])
            except ValueError:
                self._send_json_response({"error": "Invalid item ID"}, 400)
                return

            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8")
            body = json.loads(post_body)

            success, msg = gm.update_item(
                item_id=item_id,
                name=body.get("name"),
                category=body.get("category"),
                quantity=body.get("quantity"),
                price_per_unit=body.get("price_per_unit"),
                unit=body.get("unit", "units")
            )

            if success:
                dm.save_data(gm.get_budget(), gm.get_all_items())
                self._send_json_response({"success": True, "message": msg})
            else:
                self._send_json_response({"success": False, "error": msg}, 400)
            return

        self._send_json_response({"error": "Not found"}, 404)

    def do_DELETE(self):
        """Route DELETE requests for item removal."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path.startswith("/api/items/"):
            try:
                item_id = int(path.split("/")[-1])
            except ValueError:
                self._send_json_response({"error": "Invalid item ID"}, 400)
                return

            success, msg = gm.delete_item(item_id)
            if success:
                dm.save_data(gm.get_budget(), gm.get_all_items())
                self._send_json_response({"success": True, "message": msg})
            else:
                self._send_json_response({"success": False, "error": msg}, 404)
            return

        self._send_json_response({"error": "Not found"}, 404)


def run_server(port=PORT):
    """Starts the local or cloud HTTP server."""
    # Ensure working directory is the project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    is_cloud = bool(os.environ.get("RENDER") or os.environ.get("PORT"))

    server = None
    active_port = port

    if is_cloud:
        # Cloud/Render container: bind directly to assigned PORT
        server = HTTPServer((HOST, port), GroceryApiHandler)
        active_port = port
    else:
        # Local development: Try binding to requested port, fallback to alternatives
        for p in [port, 5001, 8000, 8080]:
            try:
                server = HTTPServer((HOST, p), GroceryApiHandler)
                active_port = p
                break
            except OSError:
                continue

    if not server:
        print(f"[Error] Could not bind server to port {port}. Please close running instances.")
        return

    url = f"http://{HOST}:{active_port}"
    print("\n" + "=" * 65)
    print(" 🚀 SMART GROCERY BUDGET PLANNER - WEB SERVER")
    print("=" * 65)
    print(f" • Host              : {HOST}")
    print(f" • Port              : {active_port}")
    print(f" • App URL           : {url}")
    print(f" • Health Check      : {url}/healthz")
    print(f" • REST API Endpoint : {url}/api/data")
    print(f" • Data Sync File    : {dm.filepath}")
    print("-" * 65)
    print(" Server is listening for incoming requests...")
    print("=" * 65 + "\n")

    # Automatically launch browser only in local interactive desktop environment
    if not is_cloud and not os.environ.get("CI"):
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server Stopped] Gracefully shut down.")
        server.server_close()


if __name__ == "__main__":
    run_server()
