// Formulaire de création de CV (simple).
// Utilise le endpoint /cv/ pour créer un CV.
// Peut être enrichi (wizard, multi-section, etc.) selon besoin.
import React, { useState } from "react";
import { createCV } from "../api/api";

const CVForm = () => {
  const [cvText, setCvText] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    setMessage("");
    try {
      await createCV({ data: cvText });
      setMessage("CV enregistré !");
      setCvText("");
    } catch {
      setMessage("Erreur lors de l'enregistrement du CV");
    }
  };

  return (
    <section className="mb-8">
      <h3 className="text-xl font-semibold mb-2 text-blue-700">Créer / éditer mon CV</h3>
      <form onSubmit={handleSubmit}>
        <textarea
          className="w-full border rounded p-2 mb-2"
          rows={6}
          placeholder="Copiez/collez ici le texte de votre CV ou saisissez-le..."
          value={cvText}
          onChange={e => setCvText(e.target.value)}
          required
        />
        <button className="bg-blue-700 text-white px-4 py-2 rounded hover:bg-blue-800">
          Enregistrer
        </button>
      </form>
      {message && <div className="mt-2 text-green-700">{message}</div>}
    </section>
  );
};

export default CVForm;