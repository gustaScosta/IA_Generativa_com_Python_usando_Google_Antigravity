import http.server
import socketserver
import json
import sqlite3
from urllib.parse import urlparse, parse_qs

PORT = 8000
DB_NAME = "clinica.db"


def init_db():
    """Cria o banco e as tabelas pets e agendamentos se nao existirem."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    idade TEXT NOT NULL,
                    tutor TEXT NOT NULL,
                    raca TEXT DEFAULT '',
                    contato TEXT DEFAULT ''
                )
            ''')
            # Migracao: adiciona colunas novas se o banco ja existia sem elas
            cursor.execute("PRAGMA table_info(pets)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'raca' not in columns:
                cursor.execute("ALTER TABLE pets ADD COLUMN raca TEXT DEFAULT ''")
            if 'contato' not in columns:
                cursor.execute("ALTER TABLE pets ADD COLUMN contato TEXT DEFAULT ''")

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tutor TEXT NOT NULL,
                    pet_nome TEXT NOT NULL,
                    servico TEXT NOT NULL,
                    data TEXT NOT NULL,
                    status TEXT DEFAULT 'agendado'
                )
            ''')
            conn.commit()
            print("[INFO] Banco de dados inicializado com sucesso.")
    except Exception as e:
        print("[ERRO] Falha ao inicializar o banco de dados: " + str(e))


class PetHandler(http.server.BaseHTTPRequestHandler):
    """Handler HTTP para a API de pets e agendamentos."""

    def send_json_response(self, status_code, data):
        """Envia uma resposta JSON completa com Content-Length."""
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Trata preflight CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', '0')
        self.send_header('Connection', 'close')
        self.end_headers()
        print("[OPTIONS] Preflight request em " + self.path)

    def do_GET(self):
        """Retorna dados conforme a rota."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path in ('/', '/pets'):
            self.handle_get_pets()
        elif path == '/agendamentos':
            self.handle_get_agendamentos(parsed_path)
        else:
            self.send_json_response(404, {"erro": "Rota nao encontrada"})

    def do_POST(self):
        """Cadastra dados conforme a rota."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path in ('/', '/pets'):
            self.handle_post_pet()
        elif path == '/agendamentos':
            self.handle_post_agendamento()
        else:
            self.send_json_response(404, {"erro": "Rota nao encontrada"})

    # ---------- PETS ----------

    def handle_get_pets(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, tipo, raca, nome, idade, tutor, contato FROM pets')
                rows = cursor.fetchall()
                pets = []
                for row in rows:
                    pets.append({
                        "id": row[0],
                        "tipo": row[1],
                        "raca": row[2],
                        "nome": row[3],
                        "idade": row[4],
                        "tutor": row[5],
                        "contato": row[6]
                    })
            self.send_json_response(200, pets)
            print("[GET] Lista de pets acessada. Total: " + str(len(pets)))
        except Exception as e:
            self.send_json_response(500, {"erro": "Erro interno: " + str(e)})
            print("[ERRO] Falha no GET pets: " + str(e))

    def handle_post_pet(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json_response(400, {"erro": "Corpo da requisicao vazio"})
            return
        try:
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            required_keys = ("tipo", "raca", "nome", "idade", "tutor", "contato")
            if not all(k in data for k in required_keys):
                self.send_json_response(400, {
                    "erro": "Dados incompletos. Campos obrigatorios: tipo, raca, nome, idade, tutor, contato."
                })
                return
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO pets (tipo, raca, nome, idade, tutor, contato)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (data['tipo'], data['raca'], data['nome'],
                      data['idade'], data['tutor'], data['contato']))
                conn.commit()
            self.send_json_response(201, {"mensagem": "Pet cadastrado com sucesso!"})
            print("[POST] Pet cadastrado: " + data['nome'] + " (" + data['tipo'] + " - " + data['raca'] + ")")
        except json.JSONDecodeError:
            self.send_json_response(400, {"erro": "JSON invalido"})
        except Exception as e:
            self.send_json_response(500, {"erro": "Erro interno: " + str(e)})
            print("[ERRO] Falha no POST pet: " + str(e))

    # ---------- AGENDAMENTOS ----------

    def handle_get_agendamentos(self, parsed_path):
        try:
            qs = parse_qs(parsed_path.query)
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                if 'servico' in qs:
                    cursor.execute(
                        'SELECT id, tutor, pet_nome, servico, data, status FROM agendamentos WHERE servico = ? ORDER BY data',
                        (qs['servico'][0],)
                    )
                else:
                    cursor.execute('SELECT id, tutor, pet_nome, servico, data, status FROM agendamentos ORDER BY data')
                rows = cursor.fetchall()
                agendamentos = []
                for row in rows:
                    agendamentos.append({
                        "id": row[0],
                        "tutor": row[1],
                        "pet_nome": row[2],
                        "servico": row[3],
                        "data": row[4],
                        "status": row[5]
                    })
            self.send_json_response(200, agendamentos)
            print("[GET] Lista de agendamentos acessada. Total: " + str(len(agendamentos)))
        except Exception as e:
            self.send_json_response(500, {"erro": "Erro interno: " + str(e)})
            print("[ERRO] Falha no GET agendamentos: " + str(e))

    def handle_post_agendamento(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json_response(400, {"erro": "Corpo da requisicao vazio"})
            return
        try:
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            required_keys = ("tutor", "pet_nome", "servico", "data")
            if not all(k in data for k in required_keys):
                self.send_json_response(400, {
                    "erro": "Dados incompletos. Campos obrigatorios: tutor, pet_nome, servico, data."
                })
                return
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO agendamentos (tutor, pet_nome, servico, data, status)
                    VALUES (?, ?, ?, ?, 'agendado')
                ''', (data['tutor'], data['pet_nome'], data['servico'], data['data']))
                conn.commit()
            self.send_json_response(201, {"mensagem": "Agendamento realizado com sucesso!"})
            print("[POST] Agendamento: " + data['pet_nome'] + " - " + data['servico'] + " em " + data['data'])
        except json.JSONDecodeError:
            self.send_json_response(400, {"erro": "JSON invalido"})
        except Exception as e:
            self.send_json_response(500, {"erro": "Erro interno: " + str(e)})
            print("[ERRO] Falha no POST agendamento: " + str(e))

    def log_message(self, format, *args):
        """Suprime o log padrao do BaseHTTPRequestHandler."""
        pass


class ReusableTCPServer(socketserver.TCPServer):
    """TCPServer que libera a porta imediatamente ao ser encerrado."""
    allow_reuse_address = True


if __name__ == '__main__':
    init_db()
    with ReusableTCPServer(("", PORT), PetHandler) as httpd:
        print("[INFO] Servidor rodando em http://localhost:" + str(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Servidor encerrado.")