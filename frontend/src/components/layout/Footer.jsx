// Pied de page global, moderne et pastel
import React from "react";

const Footer = () => (
  <footer className="bg-white/70 text-[#B5ADF6] py-6 mt-8 border-t border-[#A0E9E0] font-poppins">
    <div className="container mx-auto text-center text-sm font-medium">
      © {new Date().getFullYear()} SmartCV – Projet de soutenance | Tous droits réservés.
    </div>
  </footer>
);

export default Footer;