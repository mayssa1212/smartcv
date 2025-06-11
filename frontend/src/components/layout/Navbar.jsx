// Barre de navigation principale moderne et harmonisée avec le logo
import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { isAuthenticated, logoutUser } from "../../api/api";

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const handleLogout = () => {
    logoutUser();
    navigate("/login");
  };
  
  return (
    <nav className="bg-white/80 backdrop-blur shadow-md">
      <div className="container mx-auto flex justify-between items-center py-3 px-4">
        <Link to="/" className="flex items-center space-x-3">
          {/* Logo SVG intégré (adapter si tu préfères l'image dans public/) */}
          <span className="h-12 w-36 inline-block">
            <svg width="160" height="48" viewBox="0 0 400 140" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="pastelGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#A0E9E0"/>
                  <stop offset="50%" stopColor="#FBC2EB"/>
                  <stop offset="100%" stopColor="#FEE2A0"/>
                </linearGradient>
              </defs>
              <g>
                <path d="M40 100 Q55 60 70 100 Q85 140 100 100" stroke="url(#pastelGrad)" strokeWidth="8" fill="none" strokeLinecap="round"/>
                <path d="M100 100 L120 60" stroke="#B5ADF6" strokeWidth="8" strokeLinecap="round"/>
              </g>
              <text x="140" y="95" fontFamily="Poppins, Arial, sans-serif" fontSize="60" fontWeight="bold" fill="#8FD6E7" letterSpacing="2">smart</text>
              <text x="300" y="95" fontFamily="Poppins, Arial, sans-serif" fontSize="60" fontWeight="bold" fill="#FBC2EB" letterSpacing="2">cv</text>
              <text x="142" y="125" fontFamily="Poppins, Arial, sans-serif" fontSize="18" fill="#B5ADF6">by Mayssa Laffet</text>
            </svg>
          </span>
        </Link>
        <div className="flex space-x-1 md:space-x-4 font-semibold">
          <Link
            to="/"
            className={`px-3 py-2 rounded-lg transition ${
              location.pathname === "/" 
                ? "bg-[#A0E9E0] text-white" 
                : "text-[#8FD6E7] hover:bg-[#A0E9E0]/30"
            }`}
          >
            Accueil
          </Link>
          <Link
            to="/dashboard"
            className={`px-3 py-2 rounded-lg transition ${
              location.pathname === "/dashboard"
                ? "bg-[#FBC2EB] text-white"
                : "text-[#B5ADF6] hover:bg-[#FBC2EB]/30"
            }`}
          >
            Dashboard
          </Link>
          <Link
            to="/profile"
            className={`px-3 py-2 rounded-lg transition ${
              location.pathname === "/profile"
                ? "bg-[#FEE2A0] text-white"
                : "text-[#B5ADF6] hover:bg-[#FEE2A0]/30"
            }`}
          >
            Profil
          </Link>
          
          {isAuthenticated() ? (
            <button
              onClick={handleLogout}
              className={`px-3 py-2 rounded-lg transition text-[#B5ADF6] hover:bg-[#B5ADF6]/20`}
            >
              Déconnexion
            </button>
          ) : (
            <>
              <Link
                to="/login"
                className={`px-3 py-2 rounded-lg transition ${
                  location.pathname === "/login"
                    ? "bg-[#B5ADF6] text-white"
                    : "text-[#B5ADF6] hover:bg-[#B5ADF6]/20"
                }`}
              >
                Connexion
              </Link>
              <Link
                to="/register"
                className={`px-3 py-2 rounded-lg transition ${
                  location.pathname === "/register"
                    ? "bg-[#8FD6E7] text-white"
                    : "text-[#B5ADF6] hover:bg-[#8FD6E7]/30"
                }`}
              >
                Inscription
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
