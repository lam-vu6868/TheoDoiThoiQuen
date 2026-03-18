## Phần nội dung Frontend của Ứng dụng theo dõi thói quen:

👤 Thành viên đảm nhiệm chính:

- Nguyễn Tuấn Anh

## Tổng quan quy trình - Roadmap code Frontend

### Chặng 1: Setup Frontend

- [x] Khởi tạo dự án, tích hợp các thư viện đầy đủ, tích hợp Tailwind Css
- [x] Setup các biến UI (màu cho dark -light theme, các component cơ bản dễ tái sử dụng nhiều như btn, card, .....)
- [x] Setup cấu trúc thư mục, các file jsx rỗng khi truy cập các trang

### Chặng 2: Layout - Routes, Frontend Auth, Fetch API

- [ ] Code file Layout cho client, admin và dùng routes để phân các trang cho client, trang cho admin.
- [ ] Xây dựng AuthContext và AuthProvider để lưu trữ JWT, Protected Route để tránh xâm nhập ( user truy cập dashboard của Admin)
- [ ] Xây dựng Axios fetch API tiện hơn so với fetch thuần
- [ ] Xây dựng 1 Custom Hook Fetch API (Loading -- > Load Failed or Success)

### Chặng 3: Login - Signup - Logout

- [ ] Xây dựng Log in <fetch jwt từ LocalStoarge --> tạo AuthContext, Protected Route>
- [ ] Xây dựng Sign up <Fetch Api>
- [ ] Xây dựng Log out <Xóa DL trong AuthContext, xóa Jwt trên LocalStoarge>

### Chặng 4: Code UI + Fetch API Data :3

- [ ] Các Components cần tái sử dụng
- [ ] Các page cho Admin
- [ ] Các Page cho Client

# 🗿 Các thư viện sử dụng để hỗ trợ

### 1. Nhóm cơ bản

- React & React-DOM: Có sẵn khi khởi tạo dự án
- Vite: Công cụ hỗ trợ build code nhanh
- Tailwind CSS: Thư viện CSS đa dạng với các class tiện, đi kèm là các thư viện nhỏ giúp tương thích ở nhiều trình duyệt

### 2. Nhóm Điều hướng & Dữ liệu (Routing & Data)

- react-router-dom: Xử lý việc chuyển trang của REACT.
- axios: Thư viện dùng để gọi API (HTTP Client). Nó sẽ nói chuyện với Backend FastAPI để gọi EndPoint.

### 3. Nhóm Trang trí & Hiệu ứng (UI Assets)

- clsx: Giúp viết điều kiện logic cho class (ví dụ: nếu lỗi thì hiện màu đỏ).
- tailwind-merge: Giúp gộp class và xóa bỏ các class Tailwind bị trùng lặp/đánh nhau.
- react-icons: Kho chứa hàng chục ngàn icon (Facebook, Github, Mũi tên, Menu...).
- framer-motion: Thư viện làm Animation. Dùng để làm các hiệu ứng như: nội dung từ từ mờ dần hiện lên khi cuộn chuột, ảnh nảy lên khi hover...
- antd (Ant Design): Thư viện UI Component.

# 💻 Lệnh cài đặt các thư viện trên

### Kiểm tra file packeage.json để xác minh

```bash
# Lệnh Cài tailwind CSS
npm install -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p

# Lệnh cài tổng hợp các thư viện
npm install react-router-dom axios
npm install clsx tailwind-merge
npm install react-icons framer-motion
npm install antd
```

## Setup dự án

### 1. Setup Tailwind

Sau khỉ tải xong thì chỉnh các file cần thiết:

- tailwind.config.js

```bash
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- trong file index.css import các đoạn code này, sau đó import file index.css vào main.jsx

```bash
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Setup khác

Trang web tham khảo các icon của thư viện react-icons: https://react-icons.github.io/react-icons/

Trang web tham khảo các animation framer-motion: https://www.framer.com/motion/

Trang web tham khảo components antd: https://ant.design/

## Cấu trúc thư mục Frontend

```bash
├── 📁 assets         # Chứa hình ảnh, index.css
│   └── 🖼️ react.svg
├── 📁 components     # Các mảnh ghép giao diện
│   ├── 📁 common     # Các phần khung (Navbar.jsx, Footer.jsx, Sidebar.jsx)
│   └── 📁 layout
│       ├── 📄 AdminLayout.jsx  # Bố cục Layout cho trang admin
│       └── 📄 MainLayout.jsx   # Bố cục Layout cho trang Client
├── 📁 context        # Chứa AuthContext.jsx
├── 📁 hooks          # Chứa useFetch.jsx (tái sử dụng Header, gắn JWT vào header)
├── 📁 pages          # Các trang web
│   ├── 📁 admin      # Các Page Dành cho Admin
│   │   ├── 📄 .......jsx
│   └── 📁 client     # Các Page cho User
│       ├── 📄 Home.jsx
│       ├── 📄 .....jsx
│   └── 📁 common     # Các page Login, Sign Up
│       └── 📄 Login.jsx
├── 📁 routes         # Chứa AppRoutes.jsx (để cấu hình đường dẫn)
├── 📁 services       # Chứa axiosConfig.js, api.js
├── 📁 utils          # Chứa các hàm hỗ trợ (format ngày, chữ...)
├── 🎨 App.css
├── 📄 App.jsx
├── 🎨 index.css
└── 📄 main.jsx
```
