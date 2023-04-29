<script lang="ts">
  import { onMount } from "svelte";
  import logoImg from "../../assets/images/logo.png";
  import selfImg from "../../assets/images/self.png";
  import tippy from "tippy.js";
  import "tippy.js/dist/tippy.css"; // optional for styling

  let profileRef: any;

  onMount(() => {
    initialMount();
  });

  function initialMount() {
    tippy(profileRef, {
        content: "View Github",
        placement: "bottom"
    });
  }
</script>

<div class="w-full bg-stone-800 px-5 md:px-10 lg:px-20">
  <div class="w-full max-w-screen-2xl">
    <div class="flex items-center justify-between">
      <a href="/">
        <img
          src={logoImg}
          class="w-[5rem] h-[4.7rem] object-contain"
          alt="Logo"
        />
      </a>
      <a bind:this={profileRef}
        href="https://github.com/WasekSamin"
        target="_blank"
        class="w-[35px] h-[35px] rounded-full bg-stone-700 hover:bg-stone-600 transition-all duration-200 ease-linear"
      >
        <img
          src={selfImg}
          class="w-full h-full rounded-full object-contain"
          alt="Sam"
        />
      </a>
    </div>
  </div>
</div>
