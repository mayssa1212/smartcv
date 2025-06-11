// Page affichée si l'utilisateur tape une URL inconnue.
import React from "react";
import { Link } from "react-router-dom";

const NotFound = () => (
  <div className="text-center">
    <h2 className="text-3xl font-bold text-red-700 mb-2">404 - Page non trouvée</h2>
    <p className="mb-4">Oups ! Cette page n'existe pas.</p>
    <Link to="/" className="text-blue-700 underline">Retour à l'accueil</Link>
  </div>
);

export default NotFound;
