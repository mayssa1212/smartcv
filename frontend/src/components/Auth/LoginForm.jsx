import React from "react";

const LoginForm = () => (
  <form className="bg-white/90 rounded-xl shadow-lg p-6 mb-6 border border-pastelBlue max-w-md mx-auto space-y-4">
    <label className="block text-pastelLavender font-semibold mb-1">
      Email
    </label>
    <input
      type="email"
      className="border-2 border-pastelLavender focus:border-pastelAccent rounded-lg px-3 py-2 outline-none transition w-full"
      placeholder="Votre email"
    />

    <label className="block text-pastelLavender font-semibold mb-1">
      Mot de passe
    </label>
    <input
      type="password"
      className="border-2 border-pastelLavender focus:border-pastelAccent rounded-lg px-3 py-2 outline-none transition w-full"
      placeholder="Votre mot de passe"
    />

    <button
      type="submit"
      className="bg-pastelPink hover:bg-pastelAccent text-white font-semibold px-5 py-2 rounded-lg shadow transition w-full mt-4"
    >
      Connexion
    </button>
  </form>
);

export default LoginForm;