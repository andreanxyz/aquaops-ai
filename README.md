# 🐟 AquaOps AI

> AI Agent untuk manajemen peternakan ikan via WhatsApp — Garut, Jawa Barat

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-purple)](https://anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Tentang AquaOps AI

AquaOps AI adalah sistem manajemen peternakan ikan berbasis AI yang terhubung langsung via **WhatsApp** — platform yang sudah digunakan sehari-hari oleh peternak dan pekerja tambak di Indonesia.

Dirancang khusus untuk peternakan ikan di Garut, Jawa Barat.

## ✨ Fitur Utama

- 🤖 **AI Agent** — Powered by Claude (Anthropic), menjawab laporan masalah pekerja dengan panduan penanganan berdasarkan SOP budidaya
- 📱 **WhatsApp Integration** — Pekerja cukup chat via WhatsApp, tidak perlu install app baru
- 📅 **Penjadwalan Otomatis** — Tugas harian dikirim ke pekerja tepat waktu (07:00, 16:00 WIB)
- 📚 **Knowledge Base RAG** — SOP budidaya nila dan gurame tersimpan di ChromaDB
- 📊 **Laporan Harian** — Dikirim otomatis ke pemilik setiap malam (20:00 WIB)

## 🛠️ Tech Stack

| Komponen | Teknologi |
|---|---|
| Backend | Python 3.11 + FastAPI |
| AI Model | Claude (Anthropic) |
| Database | PostgreSQL + SQLAlchemy |
| Vector DB | ChromaDB |
| Messaging | WhatsApp Cloud API |
| Scheduler | APScheduler |
| Deployment | Docker + Docker Compose |

## 🚀 Quick Start

```bash
git clone https://github.com/andreanxyz/aquaops-ai.git
cd aquaops-ai
cp .env.example .env
# Edit .env dengan API keys kamu
docker-compose up -d
```

Buka API docs: `http://localhost:8000/docs`

## 📖 Contoh Interaksi

**Pekerja kirim laporan masalah:**


oh


## Contoh Interaksi

Pekerja: Pak, ikan di Kolam A nafas di permukaan terus

AquaOps AI:
DARURAT - Kemungkinan Hipoksia!
1. Nyalakan aerator SEKARANG
2. Ganti 30% air dengan air segar
3. Hitung ikan yang mati
4. Cek suhu air (idealnya 25-30C)
Pantau 30 menit. Laporkan hasilnya!

## Roadmap
- v0.1 DONE - WhatsApp, AI Agent, RAG, Auto-scheduler
- v0.2 Dashboard web untuk pemilik
- v0.3 Analisis kesehatan ikan dari foto
- v0.4 Integrasi sensor IoT

## Lisensi
MIT License - dibuat untuk peternak ikan Garut, Jawa Barat
