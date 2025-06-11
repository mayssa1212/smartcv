// Formulaire de connexion utilisateur.
// Utilise le endpoint /auth/login du backend (données x-www-form-urlencoded).
import React, { useState } from "react";
import { login } from "../../api/api";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Soumission du formulaire
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch {
      setError("Email ou mot de passe incorrect.");
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-bold mb-4 text-blue-700">Connexion</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          className="w-full border rounded p-2"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          className="w-full border rounded p-2"
          placeholder="Mot de passe"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        {error && <div className="text-red-700">{error}</div>}
        <button className="bg-blue-700 text-white px-4 py-2 rounded hover:bg-blue-800 w-full">
          Se connecter
        </button>
      </form>
    </div>
  );
};

export default Login;