import { useState, useEffect } from "react";
import {IoMdSunny} from "react-icons/io"
import {FaRegMoon} from "react-icons/fa"

const ThemeToggle = () =>{
    // Mặc định set giá trị  theme là light nếu như chưa có theme
    const [theme, setTheme] = useState(() => {
        localStorage.getItem('theme') || 'light';
    });

    // === Bắt sự kiện khi biến theme state thay đổi 
    useEffect(()=>{
        const htmlElement = document.documentElement;
        if(theme === 'dark'){
            htmlElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        }
        else{
            htmlElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }, [theme]);

    const toggleTheme = () =>{
        setTheme(theme === 'light' ? 'dark' : 'light');
    };

    return (
        <button onClick={toggleTheme} className="btn-primary flex items-center transition-all duration-500 ease-linear gap-2">
            {
                theme === 'light'
                ?(
                    <>
                    Light <IoMdSunny className="text-xl"/>
                    </>
                )
                :(
                    <>
                    Dark <FaRegMoon className="text-xl"/>
                    </>
                )
            }
        </button>
    )
}
export default ThemeToggle