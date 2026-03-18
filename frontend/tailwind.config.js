/** @type {import('tailwindcss').Config} */
export default {
  // Kích hoạt Dark Mode bằng class 
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
// ========================== THIẾT LẬP MÀU SẮC 
      colors:{
//---------------- Màu chủ đạo (nút bấm, viền, hiệu ứng hover)
        primary:{
          DEFAULT: '#00d2d3', // Màu chính của trang web
          hover: '#01a3a4',   // Màu chính khi hover vào 
        },
//---------------- Nhóm màu cho chế độ light
        light:{
            bg: '#f8f9fa',        // Màu nền tổng thể toàn trang 
            surface: '#ffffff',   // Màu nền các khối hộp (Card, Navbar)
            text: '#2d3436',      // Màu chữ chính
            muted: '#636e72'      // Mãu chữ phụ (Mô tả, ngày tháng,...)
        },
//---------------- Nhóm màu cho chế độ dark 
        dark:{
            bg: '#111827',        // Màu nền tổng thể toàn trang 
            surface: '#1f2937',   // Màu nền các khối hộp (Card, Navbar)
            text: '#f9fafb',      // Màu chữ chính
            muted: '#9ca3af'      // Mãu chữ phụ (Mô tả, ngày tháng,...)
        },
      },
//================ THIẾT LẬP FONT CHỮ 
      fontFamily:{
        sans: ["Inter", "system-ui", "sans-serif"],
      }
    },
  },
  plugins: [],
}