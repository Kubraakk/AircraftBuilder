# Hava Aracı Üretim Uygulaması

Hava aracı üretim süreçlerinin yönetilmesi için geliştirilmiş bir sistemdir.Uygulama takımların belirli uçakları üretmesini, stok yönetimi yapmasını ve montaj sürecini takip etmesini sağlar.Her takım yalnızca kendi sorumluluğundaki parçaları üretebilir ve montaj ekibi, tamamlanmış parçalarla uçakları birleştirebilir.

## Projenin amacı

- Hava aracı üretim sürecinin dijitalleştirilmesi ve takip edilebilir hale getirilmesi.
- Takım bazlı üretim modeli ile her ekibin kendi sorumluluğunu yerine getirmesi.
- Envanter yönetimi ve eksik parça uyarıları ile verimli üretim süreci sağlamak.
- Montaj sürecinin yönetilmesi ve üretilen uçakların sistem üzerinden takip edilmesi.

## Fonksiyonlar

### Personel & Takım Yönetimi

✅ Kullanıcılar sisteme giriş yapabilir.<br>
✅ Her personelin belirli bir takımı vardır. (Aviyonik, Kanat, Gövde, Kuyruk, Montaj)<br>
✅ Bir takımda birden fazla personel bulunabilir.

### Parça Üretimi ve Yönetimi

✅ Takımlar, yalnızca kendi sorumluluklarındaki parçaları üretebilir.<br>
✅ Üretilen parçalar CRUD (Create, Read, Update, Delete) işlemlerine tabidir.<br>
✅ Her parça, yalnızca belirli bir uçakta kullanılabilir (Örn: TB2 kanadı, TB3 için kullanılamaz).

### Montaj Süreci

✅ Montaj ekibi, tamamlanmış parçaları birleştirerek uçak üretir.<br>
✅ Eksik parçalar varsa sistem uyarı verir (Örn: Akıncı için gövde eksik).<br>
✅ Montaj tamamlandığında stok güncellenir ve kullanılan parçalar envanterden düşülür.<br>
✅ Montajı tamamlanan uçaklar listelenebilir.

## Kullanılan Teknolojiler

- Python --> Backend geliştirme için kullanıldı
- Django --> Web uygulamasının çatısı (framework)
- Django Rest Framework (DRF) -->API geliştirme
- PostgreSQL --> Veritabanı yönetimi
- Docker --> Uygulamanın konteynerize edilmesi
- HTML / CSS (Bootstrap) --> Kullanıcı arayüzü geliştirme
- JavaScript (Fetch API) --> API ile etkileşim sağlama
- jQuery & DataTables --> Dinamik tablo işlemleri ve veri listeleme

## Kurulum & Çalıştırma

Projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1️⃣ Projeyi Klonlayın

```bash
git clone https://github.com/Kubraakk/AircraftBuilder.git
cd AircraftBuilder
```

2️⃣ Docker ile Çalıştırın

```bash
docker-compose up --build
```

📌 Not: docker-compose.yml dosyasında PostgreSQL ve uygulama servisleri yer almaktadır.

3️⃣ Veritabanı Migration İşlemleri

```bash
docker compose run --rm app sh -c "python manage.py migrate"
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

📌 Not: Süper kullanıcı oluşturduktan sonra admin panelinden giriş yapabilirsiniz.

4️⃣ Uygulamayı Çalıştırın

```bash
docker compose up
```

Artık uygulama aşağıdaki adreste çalışıyor olacak:<br>
🌍 Frontend: http://127.0.0.1:8000/userpanel/login/<br>
⚙️ Admin Panel: http://127.0.0.1:8000/admin/<br>
📜 API Dokümantasyonu: http://127.0.0.1:8000/api/docs/

## 🔗 API Endpointleri

| HTTP Yöntemi | URL                             | Açıklama                       |
| ------------ | ------------------------------- | ------------------------------ |
| **POST**     | `/api/auth/login/`              | Kullanıcı girişi yapar         |
| **POST**     | `/api/auth/register/`           | Yeni kullanıcı kaydı oluşturur |
| **GET**      | `/api/auth/me/`                 | Kullanıcı bilgilerini getirir  |
| **GET**      | `/api/parts/inventory/`         | Envanterdeki parçaları getirir |
| **GET**      | `/api/parts/parts/`             | Eklenen parçaları listeler     |
| **POST**     | `/api/parts/parts/`             | Yeni parça ekler               |
| **DELETE**   | `/api/parts/parts/{id}/`        | Bir parçayı sistemden siler    |
| **UPDATE**   | `/api/parts/parts/{id}/`        | Bir parçayı günceller          |
| **GET**      | `/api/parts/assembly/`          | Montaj işlemlerini listeler    |
| **POST**     | `/api/parts/assembly/assemble/` | Montaj işlemini başlatır       |

## API Yanıtları

### Kullanıcı Bilgisi Getirme\*\*

**POST** `/api/auth/login/`

```json
{
  "email": "kanat@example.com",
  "password": "12345"
}
```

**Yanıt(Response)**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTk1ODE4MSwiaWF0IjoxNzM5MzUzMzgxLCJqdGkiOiI1NmNmNWMxZGVmOWU0YmEyYjAyMTQ1ZWZhZjFjMmYyNCIsInVzZXJfaWQiOjZ9.QjdH7XyKQUjlC8b65ZQdpn8da7l2pgwPh3JFUemcpSw",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5MzYwNTgxLCJpYXQiOjE3MzkzNTMzODEsImp0aSI6ImVhZDAxMzczNjk2NjQzYTZiN2EyZjdkMjI1YjY5YjlkIiwidXNlcl9pZCI6Nn0.b6RyOBp66Ul0iQNtsJI97OJAxitf2lIYzRJlk61AT1s"
}
```

**POST** `/api/auth/register/`

```json
{
  "email": "kanat@example.com",
  "first_name": "Ali",
  "last_name": "Veli",
  "password": "12345",
  "team": 1
}
```

**Yanıt(Response)**

```json
{
  "id": 2,
  "email": "kanat@example.com",
  "first_name": "Ali",
  "last_name": "Veli",
  "team": "Kanat Takımı"
}
```

**POST** `/api/parts/parts`

```json
{
  "name": "Kanat",
  "aircraft": 1,
  "team": 1
}
```

**Yanıt(Response)**

```json
{
  "id": 8,
  "name": "Kanat",
  "aircraft": 1,
  "team": 1,
  "quantity": 1
}
```

**Uyuşmayan Takım ve Parça Durumunda Response**

```json
{
  "error": "Aviyonik Takımı Kanat üretemez!"
}
```

**GET** `/api/parts/inventory/`
**Yanıt(Response)**

```json
[
  {
    "id": 1,
    "part_name": "Kanat",
    "aircraft_name": "Bayraktar TB2",
    "quantity": 2
  },
  {
    "id": 5,
    "part_name": "Gövde",
    "aircraft_name": "Bayraktar TB2",
    "quantity": 1
  },
  {
    "id": 7,
    "part_name": "Aviyonik",
    "aircraft_name": "Bayraktar TB2",
    "quantity": 1
  }
]
```

**GET** `/api/parts/assembly/`
**Yanıt(Response)**

```json
[
  {
    "id": 1,
    "aircraft": 1,
    "aircraft_name": "Bayraktar TB2",
    "parts_used": [
      {
        "part_name": "Kanat",
        "quantity_used": 2
      },
      {
        "part_name": "Gövde",
        "quantity_used": 1
      },
      {
        "part_name": "Kuyruk",
        "quantity_used": 1
      },
      {
        "part_name": "Aviyonik",
        "quantity_used": 1
      }
    ],
    "created_at": "2025-02-11T20:21:50.431296Z"
  }
]
```

**POST** `/api/parts/assembly/assemble/`

```json
{
  "aircraft": 1
}
```

**Başarılı Yanıt(Response)**

```json
{
  "id": 2,
  "aircraft_name": "Bayraktar TB2",
  "status": "Montaj tamamlandı"
}
```

**Eksik Parça Durumunda Yanıt(Response)**

```json
{
  "error": "Eksik parçalar: Kanat (2 eksik)"
}
```

## Ekran Görüntüleri

![Login](app/userpanel/static/images/login.png) <br>

![Login](app/userpanel/static/images/montaj.png) <br>

![Login](app/userpanel/static/images/montaj-hata.png) <br>

![Login](app/userpanel/static/images/ucaklar.png) <br>
