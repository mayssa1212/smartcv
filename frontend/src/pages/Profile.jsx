import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Simuler la récupération des données utilisateur
    // Remplacez ceci par un vrai appel API pour récupérer les données utilisateur
    const fetchUser = async () => {
      try {
        // Exemple: const response = await fetch('/api/user/profile');
        // const data = await response.json();
        
        // Pour le moment, utilisons des données fictives
        const mockUser = {
          full_name: "Utilisateur Test",
          email: "utilisateur@example.com"
        };
        
        setUser(mockUser);
        setLoading(false);
      } catch (error) {
        console.error("Erreur lors de la récupération du profil:", error);
        setLoading(false);
        // Rediriger vers la page de connexion si non authentifié
        // navigate('/login');
      }
    };

    fetchUser();
  }, []);

  if (loading) {
    return (
      <div className="max-w-xl mx-auto mt-10 text-center">
        <p className="text-pastelAccent">Chargement du profil...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="max-w-xl mx-auto mt-10 text-center">
        <p className="text-red-500">Impossible de charger le profil. Veuillez vous connecter.</p>
        <button 
          onClick={() => navigate('/login')}
          className="mt-4 bg-pastelPink hover:bg-pastelAccent text-white font-bold px-4 py-2 rounded-xl"
        >
          Se connecter
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto mt-10">
      <div className="bg-white/90 rounded-xl shadow-lg p-6 mb-6 border border-pastelBlue">
        <h2 className="text-xl font-bold text-pastelAccent mb-2">Profil utilisateur</h2>
        <p className="text-pastelLavender">{user.full_name}</p>
        <p className="text-pastelLavender">{user.email}</p>
      </div>
    </div>
  );
};

export default Profile;
