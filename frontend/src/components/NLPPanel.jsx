// Petit guide d'utilisation pour la page d'accueil.
import React from "react";

const NLPGuide = () => (
  <section className="bg-blue-50 p-6 rounded-lg shadow">
    <h2 className="text-xl font-semibold mb-2 text-blue-700">Comment utiliser l'analyse NLP ?</h2>
    <ol className="list-decimal list-inside space-y-1 text-gray-700">
      <li>Créez un compte ou connectez-vous.</li>
      <li>Remplissez votre CV ou importez-le.</li>
      <li>Lancez l'analyse pour détecter vos compétences, expériences, etc.</li>
      <li>Visualisez les résultats et optimisez votre CV grâce aux conseils IA.</li>
      <li>Téléchargez ou partagez votre CV amélioré !</li>
    </ol>
  </section>
);

export default NLPGuide;
