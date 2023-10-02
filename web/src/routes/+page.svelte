<script lang="ts">
  import { enhance } from "$app/forms"

  function sendForm() {}
</script>

<ol class="list-decimal px-4 text-center flex flex-col gap-2">
  <li>Renseigne tes coordonnées avec le numéro associé à ton compte Lydia</li>
  <li>
    Notre bot s'occupe de lancer la réservation de ta place à 13h pétantes
  </li>
  <li>Valide le paiement depuis ton appli Lydia</li>
  <li>Tes données sont supprimées directement après le shotgun</li>
</ol>
<form class="flex flex-col gap-4 w-full lg:px-6" method="POST" use:enhance>
  <label class="w-full" for="lastName">
    <p class="text-gray-700">Nom</p>
    <input
      id="lastName"
      class="p-2 rounded-lg border w-full"
      name="lastName"
      placeholder="Tornado"
      required
    />
  </label>
  <label class="w-full" for="firstName">
    <p class="text-gray-700">Prénom</p>
    <input
      id="firstName"
      class="p-2 rounded-lg border w-full"
      name="firstName"
      placeholder="Johnny"
      required
    />
  </label>
  <label class="w-full" for="email">
    <p class="text-gray-700">Adresse email</p>
    <input
      id="email"
      class="p-2 rounded-lg border w-full"
      name="email"
      type="email"
      placeholder="johnny.tornado@wanadoo.fr"
      required
    />
  </label>
  <label class="w-full" for="phone">
    <p class="text-gray-700">Portable (associé au compte Lydia)</p>
    <input
      id="phone"
      class="p-2 rounded-lg border w-full"
      name="phone"
      placeholder="06XXXXXX89"
      required
    />
  </label>
  <button class="bg-pink-600 px-4 py-2 mt-2" type="submit">
    <span class="text-white font-bold italic">Shotgun !</span>
  </button>
</form>
