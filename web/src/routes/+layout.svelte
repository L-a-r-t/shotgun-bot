<script lang="ts">
  import "../app.css"
</script>

<div class="w-full min-h-screen h-full p-4 pb-12 bg-cyan-950">
  <h1
    class="font-extrabold italic text-7xl text-center text-pink-600 drop-shadow-[0_0_15px_rgba(219,39,119,0.7)]"
  >
    Shotgunator
  </h1>
  <p class="text-center text-pink-600 italic">
    Ne rate pas le shotgun du <span class="border-b-2 border-white text-white"
      >Quadrabang</span
    >
  </p>
  <div
    class="max-w-xl mx-auto mt-6 flex flex-col items-center gap-8 py-8 px-12 bg-white shadow-xl"
  >
    <slot />
  </div>
</div>
<p class="text-white text-sm bg-cyan-950 p-4 text-center">
  Shotgunator est un outil gratuit et open-source développé par Théo Lartigau et
  Rémy Siahaan. Le lien vers le GitHub est le suivant: <a
    href="https://github.com/L-a-r-t/shotgun-bot"
    target="_blank"
    class="underline">https://github.com/L-a-r-t/shotgun-bot</a
  >. Nous nous engagons à ne communiquer aucune donnée avec un tiers et à les
  supprimer automatiquement après usage de l'outil.
</p>
