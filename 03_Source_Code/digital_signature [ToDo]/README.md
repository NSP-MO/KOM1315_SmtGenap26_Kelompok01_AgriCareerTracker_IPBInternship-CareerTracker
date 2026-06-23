# Modul Digital Signature (JWS/JWT)
**AgriCareer-Tracker**

Modul ini memuat demonstrasi implementasi mekanisme **Digital Signature** otentik yang diadopsi langsung dari basis kode *AgriCareer-Tracker* (secara spesifik merujuk pada fungsi otentikasi di `auth.py` dan aktivasi akun di `mailer.py`).

Sistem AgriCareer menggunakan pendekatan **JSON Web Signature (JWS)** yang terenkapsulasi dalam format **JWT (JSON Web Token)**. Implementasi ini menggunakan algoritma kunci simetris **HMAC-SHA256 (HS256)** guna menjamin integritas data serta memenuhi aspek *non-repudiation* (nirsangkal) dalam transmisi data antara klien dan server.

## Spesifikasi Teknis
- **Bahasa Pemrograman**: Python 3.11+
- **Pustaka Kriptografi Utama**: `python-jose`
- **Algoritma Hashing/Penandatanganan**: HS256 (HMAC-SHA256)

## Konsep Operasional
1. **Signing (Penandatanganan)**: Modul `jwt_signer.py` mensimulasikan proses di mana REST API (server) mengenkapsulasi identitas pengguna (payload) dan menandatanganinya menggunakan *Secret Key* internal. Proses ini menghasilkan *Bearer Token* yang memuat *Digital Signature* sah.
2. **Verifying (Verifikasi Integritas)**: Modul `jwt_verifier.py` bertugas memvalidasi otentisitas token. Apabila terdapat modifikasi sekecil apa pun pada *header* atau *payload* di sisi klien (manipulasi data), perhitungan algoritma *hash* akan mengalami ketidakcocokan. Hal ini secara otomatis akan memicu eksepsi (`JWTError`), sehingga sistem dapat memitigasi serangan pemalsuan data (*Forgery*).

## Instruksi Pengujian Modul (Simulasi)
Pastikan pustaka `python-jose` dan `python-dotenv` telah terinstal di lingkungan Anda (rujuk pada berkas `requirements.txt`).

Jalankan skrip demonstrasi melalui perintah berikut:
```bash
python demo_jwt.py
```
Skrip tersebut akan memvisualisasikan alur keamanan berikut:
1. Penerbitan token otentikasi untuk entitas pengguna "mahasiswa".
2. Proses verifikasi hak akses yang berhasil dilakukan oleh server.
3. Simulasi eksploitasi di mana pihak eksternal memodifikasi nilai struktur _base64_ pada token untuk melakukan eskalasi hak akses menjadi "admin".
4. Kegagalan verifikasi oleh server dikarenakan _Signature_ token tidak memiliki kesesuaian matematis dengan _payload_ termodifikasi, membuktikan ketahanan sistem terhadap serangan.
