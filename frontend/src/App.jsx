import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";

// Pages
const Home = () => <div className="p-4"><h1 className="text-2xl font-bold">Accueil</h1><p>Bienvenue sur SmartCV</p></div>;
const Dashboard = () => <div className="p-4"><h1 className="text-2xl font-bold">Dashboard</h1><p>Votre tableau de bord</p></div>;
const Profile = () => <div className="p-4"><h1 className="text-2xl font-bold">Profil</h1><p>Votre profil utilisateur</p></div>;
const Login = () => <div className="p-4"><h1 className="text-2xl font-bold">Connexion</h1><p>Connectez-vous à votre compte</p></div>;
const Register = () => <div className="p-4"><h1 className="text-2xl font-bold">Inscription</h1><p>Créez un nouveau compte</p></div>;
const NotFound = () => <div className="p-4"><h1 className="text-2xl font-bold">404</h1><p>Page non trouvée</p></div>;

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-gray-50">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
