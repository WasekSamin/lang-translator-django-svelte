<script>
    import "../app.css";
    import logoImg from "../assets/images/logo.png";
</script>

<slot />

<svelte:head>
  <link rel="icon" href={logoImg} />
</svelte:head>