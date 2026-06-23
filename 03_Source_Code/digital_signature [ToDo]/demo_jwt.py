import json
import base64
from jwt_signer import create_access_token
from jwt_verifier import decode_token

def tamper_jwt_payload(token: str, new_role: str) -> str:
    """
    Mensimulasikan kerentanan (Tampering) di mana pihak eksternal memodifikasi bagian payload 
    token JWT secara tidak sah (contoh: eskalasi hak akses / privilege escalation).
    """
    parts = token.split(".")
    if len(parts) != 3:
        return token
        
    header, payload, signature = parts
    
    # Menambahkan padding base64
    payload_padded = payload + '=' * (-len(payload) % 4)
    decoded_payload = json.loads(base64.urlsafe_b64decode(payload_padded).decode('utf-8'))
    
    # Manipulasi data secara tidak sah
    print(f"   [UNAUTHORIZED_MODIFICATION] Memodifikasi hak akses dari '{decoded_payload.get('role')}' menjadi '{new_role}'...")
    decoded_payload["role"] = new_role
    
    # Encode ulang ke base64 (tanpa padding '=')
    tampered_payload = base64.urlsafe_b64encode(json.dumps(decoded_payload).encode('utf-8')).decode('utf-8').rstrip('=')
    
    # Gabungkan header + tampered payload + old signature (Signature tetap, karena Secret Key tidak diketahui eksternal)
    tampered_token = f"{header}.{tampered_payload}.{signature}"
    return tampered_token

def run_demo():
    print("="*70)
    print("PENGUJIAN MODUL DIGITAL SIGNATURE (JSON WEB SIGNATURE / JWT)")
    print("Mekanisme Autentikasi dan Non-Repudiation pada AgriCareer-Tracker")
    print("="*70)
    
    # 1. Penerbitan kredensial pengguna
    print("\n[TAHAP 1] Server menerbitkan Token Otentikasi Pengguna")
    user_data = {
        "sub": "mahasiswa123",
        "role": "mahasiswa",
        "name": "Budi Santoso"
    }
    
    token = create_access_token(user_data)
    print(f"Token berhasil diterbitkan dan ditandatangani (Signature HS256).")
    print(f"   >>> Token Klien: {token[:30]}...{token[-30:]}")
    
    # 2. Verifikasi akses sah
    print("\n[TAHAP 2] Klien dengan Otoritas Sah Mengakses REST API")
    print("   Sistem memverifikasi integritas Signature (Mengecek otentisitas penerbit)...")
    valid_payload = decode_token(token)
    if valid_payload:
        print(f"STATUS VALID: Signature Terverifikasi. Akses diizinkan untuk entitas: {valid_payload.get('name')}.")
    
    # 3. Simulasi manipulasi data (Tampering)
    print("\n[TAHAP 3] Entitas Tidak Sah Melakukan Manipulasi Token (Data Forgery)")
    tampered_token = tamper_jwt_payload(token, "admin")
    
    # 4. Verifikasi akses ilegal
    print("\n[TAHAP 4] Entitas Tidak Sah Meminta Akses dengan Token Termodifikasi")
    print("   Sistem melakukan verifikasi ulang integritas Signature...")
    invalid_payload = decode_token(tampered_token)
    if invalid_payload is None:
        print("AKSES DITOLAK: Kegagalan validasi Signature. Sistem mendeteksi adanya manipulasi data (Tampering).")
        
    print("\n" + "="*70)
    print("PENGUJIAN SELESAI")
    print("Mekanisme JWS terbukti efektif melindungi integritas data dan mencegah penyangkalan (Non-repudiation).")
    print("="*70)

if __name__ == "__main__":
    run_demo()
