import { motion } from "framer-motion";
import { FaRocket } from "react-icons/fa"; // Import icon tên lửa

export default function App() {
  return (
    // Thẻ bọc ngoài cùng: Full màn hình, nền tối, căn giữa mọi thứ
    <div className="min-h-screen flex items-center justify-center bg-slate-900 font-sans p-4">
      
      {/* 1. Khung Card chính: Trượt từ dưới lên (y: 50 -> y: 0) */}
      <motion.div 
        initial={{ opacity: 0, y: 50 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="bg-slate-800 p-10 rounded-3xl shadow-2xl flex flex-col items-center gap-6 max-w-sm text-center border border-slate-700"
      >
        
        {/* 2. Icon Tên lửa: Xoay 360 độ lặp lại vô hạn */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
          className="p-5 bg-blue-500/20 rounded-full text-blue-400 text-6xl"
        >
          <FaRocket />
        </motion.div>

        {/* 3. Phần chữ: Dùng class Tailwind để tô màu và chỉnh size */}
        <div>
          <h1 className="text-2xl font-bold text-white mb-3">
            Setup Thành Công! 🎉
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed">
            Tailwind CSS, React Icons và Framer Motion đều đang hoạt động hoàn hảo. Hệ thống đã sẵn sàng 100%.
          </p>
        </div>

        {/* 4. Nút bấm: Có hiệu ứng phóng to khi đưa chuột vào (whileHover) và lún xuống khi bấm (whileTap) */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-8 rounded-xl w-full transition-colors"
        >
          Bắt đầu Code Frontend! Nhưng cần tìm hiểu nhiều hơn sao cho code tối ưu và làm việc hiệu quả nhất!
        </motion.button>

      </motion.div>

    </div>
  );
}