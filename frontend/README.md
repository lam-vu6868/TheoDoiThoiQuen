## Phần nội dung Frontend của Ứng dụng theo dõi thói quen:

👤 Thành viên đảm nhiệm chính:

- Nguyễn Tuấn Anh

## Tổng quan quy trình - Roadmap code Frontend

### Chặng 1: Setup Frontend

- [ ] Khởi tạo dự án, tích hợp các thư viện đầy đủ, tích hợp Tailwind Css
- [ ] Setup các biến UI (màu cho dark -light theme, các component cơ bản dễ tái sử dụng nhiều như btn, card, .....)
- [ ] Setup cấu trúc thư mục, các file jsx rỗng khi truy cập các trang

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
