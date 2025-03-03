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

5️⃣ Testleri Çalıştırın

```bash
docker compose run --rm app sh -c "python manage.py test"
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


