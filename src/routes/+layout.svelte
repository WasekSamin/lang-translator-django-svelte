<script>
  import "../app.css";
  import logoImg from "../assets/images/logo.png";
</script>

<slot />

<svelte:head>
  <link rel="icon" href={logoImg} />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Poppins&display=swap"
    rel="stylesheet"
  />
</svelte:head>
