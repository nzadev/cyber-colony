import os
import json
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "reviews.json")
ANNOUNCEMENT_FILE = os.path.join(BASE_DIR, "announcement.json")
CHAT_FILE = os.path.join(BASE_DIR, "developer_inbox.json")
ADMIN_PIN = "8888" # Default Admin Passcode PIN

def load_reviews():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_reviews(reviews):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def load_announcement():
    if not os.path.exists(ANNOUNCEMENT_FILE):
        default_data = {
            "active": True,
            "text": "🔥 Protocol Zero (Prototype v1.5.0): Fitur Multiplayer Co-Op & Kontrol Gerak Besar Resmi Aktif!",
            "updated_at": datetime.now().strftime("%d %b %Y, %H:%M WIB")
        }
        with open(ANNOUNCEMENT_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
        return default_data
    try:
        with open(ANNOUNCEMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"active": False, "text": "", "updated_at": ""}

def save_announcement(data):
    with open(ANNOUNCEMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_chat():
    if not os.path.exists(CHAT_FILE):
        default_chat = [
            {
                "id": 1,
                "sender": "Antigravity AI (Dev)",
                "role": "bot",
                "message": "Halo Atmin! 🤖 Ruang chat developer ini langsung terhubung ke sistem server lokal. Kamu bisa ketik ide update, laporan bug, atau request fitur di sini kapan saja!",
                "time": datetime.now().strftime("%d %b %Y, %H:%M WIB")
            }
        ]
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(default_chat, f, ensure_ascii=False, indent=2)
        return default_chat
    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_chat(chats):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)

class CommunityHubHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ["/admin", "/admin/"]:
            admin_path = os.path.join(BASE_DIR, "admin.html")
            if os.path.exists(admin_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(admin_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if parsed.path == "/api/reviews":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            reviews = load_reviews()
            self.wfile.write(json.dumps(reviews, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/api/announcement":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            ann = load_announcement()
            self.wfile.write(json.dumps(ann, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/api/admin/chat":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            chats = load_chat()
            self.wfile.write(json.dumps(chats, ensure_ascii=False).encode("utf-8"))
            return
            
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        if parsed.path == "/api/reviews":
            try:
                data = json.loads(body)
                name = str(data.get("name", "")).strip()[:40]
                category = str(data.get("category", "💣 Kritik Pedas & Evaluasi")).strip()
                rating = max(1, min(5, int(data.get("rating", 5))))
                fav_class = str(data.get("favClass", "Vanguard Commando")).strip()[:40]
                comment = str(data.get("comment", "")).strip()
                
                # Limit to 60 words
                words = comment.split()
                if len(words) > 60:
                    comment = " ".join(words[:60])
                comment = comment[:350]

                if not name or not comment:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Name and comment required"}')
                    return

                now_str = datetime.now().strftime("%d %b %Y, %H:%M WIB")
                new_entry = {
                    "id": int(time.time() * 1000),
                    "name": name,
                    "category": category,
                    "rating": rating,
                    "favClass": fav_class,
                    "comment": comment,
                    "likes": 0,
                    "liked_by": [],
                    "is_pinned": False,
                    "admin_reply": None,
                    "time": now_str
                }

                reviews = load_reviews()
                reviews.insert(0, new_entry)
                save_reviews(reviews)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "reviews": reviews}, ensure_ascii=False).encode("utf-8"))
                print(f"[NEW REVIEW] from {name}: {comment}")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        elif parsed.path == "/api/reviews/like":
            try:
                data = json.loads(body)
                review_id = data.get("id")
                client_id = str(data.get("clientId", "")).strip()
                if not client_id:
                    client_id = self.client_address[0]

                reviews = load_reviews()
                updated_likes = 0
                has_liked = False

                for r in reviews:
                    if r.get("id") == review_id:
                        if "liked_by" not in r:
                            r["liked_by"] = []

                        if client_id in r["liked_by"]:
                            r["liked_by"].remove(client_id)
                            has_liked = False
                        else:
                            r["liked_by"].append(client_id)
                            has_liked = True

                        r["likes"] = len(r["liked_by"])
                        updated_likes = r["likes"]
                        break

                save_reviews(reviews)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True, 
                    "id": review_id, 
                    "likes": updated_likes, 
                    "hasLiked": has_liked
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
            return

        # ADMIN ENDPOINTS
        elif parsed.path == "/api/admin/delete":
            try:
                data = json.loads(body)
                pin = str(data.get("pin", "")).strip()
                if pin not in ["8888", ADMIN_PIN, "admin", "nza"]:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "PIN Admin salah! (Default PIN: 8888)"}).encode("utf-8"))
                    return

                del_id = str(data.get("id", "")).strip()
                reviews = load_reviews()
                before_count = len(reviews)
                reviews = [r for r in reviews if str(r.get("id")) != del_id]
                save_reviews(reviews)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "reviews": reviews, "deleted": before_count - len(reviews)}, ensure_ascii=False).encode("utf-8"))
                print(f"[ADMIN DELETED] Feedback ID {del_id}")
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        elif parsed.path == "/api/admin/reply":
            try:
                data = json.loads(body)
                pin = str(data.get("pin", "")).strip()
                if pin not in ["8888", ADMIN_PIN, "admin", "nza"]:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "PIN Admin salah!"}).encode("utf-8"))
                    return

                target_id = str(data.get("id", "")).strip()
                reply_text = str(data.get("reply", "")).strip()
                if not reply_text:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Teks balasan tidak boleh kosong"}).encode("utf-8"))
                    return

                now_str = datetime.now().strftime("%d %b %Y, %H:%M WIB")
                reviews = load_reviews()
                for r in reviews:
                    if str(r.get("id")) == target_id:
                        r["admin_reply"] = {
                            "text": reply_text,
                            "time": now_str,
                            "author": "👑 Developer (Atmin)"
                        }
                        break
                save_reviews(reviews)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "reviews": reviews}, ensure_ascii=False).encode("utf-8"))
                print(f"[ADMIN REPLIED] to ID {target_id}: {reply_text}")
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        elif parsed.path == "/api/admin/pin":
            try:
                data = json.loads(body)
                pin = str(data.get("pin", "")).strip()
                if pin not in ["8888", ADMIN_PIN, "admin", "nza"]:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "PIN Admin salah!"}).encode("utf-8"))
                    return

                target_id = str(data.get("id", "")).strip()
                reviews = load_reviews()
                for r in reviews:
                    if str(r.get("id")) == target_id:
                        r["is_pinned"] = not r.get("is_pinned", False)
                        break
                save_reviews(reviews)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "reviews": reviews}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        elif parsed.path == "/api/admin/announcement":
            try:
                data = json.loads(body)
                pin = str(data.get("pin", "")).strip()
                if pin not in ["8888", ADMIN_PIN, "admin", "nza"]:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "PIN Admin salah!"}).encode("utf-8"))
                    return

                text = str(data.get("text", "")).strip()
                active = bool(data.get("active", True))
                ann_data = {
                    "active": active,
                    "text": text,
                    "updated_at": datetime.now().strftime("%d %b %Y, %H:%M WIB")
                }
                save_announcement(ann_data)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "announcement": ann_data}, ensure_ascii=False).encode("utf-8"))
                print(f"[ANNOUNCEMENT UPDATED] {text}")
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        elif parsed.path == "/api/admin/chat":
            try:
                data = json.loads(body)
                pin = str(data.get("pin", "")).strip()
                if pin not in ["8888", ADMIN_PIN, "admin", "nza"]:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "PIN Admin salah!"}).encode("utf-8"))
                    return

                msg_text = str(data.get("message", "")).strip()
                if not msg_text:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Pesan tidak boleh kosong"}).encode("utf-8"))
                    return

                now_str = datetime.now().strftime("%d %b %Y, %H:%M WIB")
                chats = load_chat()
                
                admin_msg = {
                    "id": int(time.time() * 1000),
                    "sender": "Atmin (Creator)",
                    "role": "admin",
                    "message": msg_text,
                    "time": now_str
                }
                chats.append(admin_msg)

                # Automatic developer AI receipt
                auto_reply = {
                    "id": int(time.time() * 1000) + 1,
                    "sender": "Antigravity AI (Dev)",
                    "role": "bot",
                    "message": f"✅ Pesan dicatat di database server: \"{msg_text}\". Developer AI akan membaca dan memproses saat instruksi berikutnya dijalankan!",
                    "time": now_str
                }
                chats.append(auto_reply)

                # Keep last 50 chat messages
                if len(chats) > 50:
                    chats = chats[-50:]

                save_chat(chats)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "chats": chats}, ensure_ascii=False).encode("utf-8"))
                print(f"[ADMIN CHAT INBOX] {msg_text}")
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        elif parsed.path == "/api/admin/clear":
            try:
                data = json.loads(body)
                pin = str(data.get("pin", "")).strip()
                if pin not in ["8888", ADMIN_PIN, "admin", "nza"]:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "PIN Admin salah!"}).encode("utf-8"))
                    return

                save_reviews([])
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "reviews": []}, ensure_ascii=False).encode("utf-8"))
                print("[ADMIN CLEARED ALL FEEDBACKS]")
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), CommunityHubHandler)
    print(f"🚀 Real Community Hub Server running on http://0.0.0.0:{PORT} with Admin API & JSON DB")
    server.serve_forever()
