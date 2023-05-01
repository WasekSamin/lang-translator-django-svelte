<script lang="ts">
  import { afterUpdate } from "svelte";
  import Icon from "@iconify/svelte";
  import { createEventDispatcher } from "svelte";
  import { scale } from "svelte/transition";
  import { quintOut } from "svelte/easing";
  import { COUNTRIES } from "../ts/country";

  const dispatch = createEventDispatcher();

  $: countries = [...COUNTRIES];

  export let isSrcCountryOptionSelected: boolean;

  let modalTopRef: any, searchCountryInputRef: any, 
    countryListRef: any, countrySelectModalRef: any;
  let countrySearchInput: string = "";

  function handleWindowKeyup(e: any) {
    if (e.key === "Escape") {
        closeCountryModal();
    }
  }

  function handleWindowClick(e: any) {
    if (!e.target.contains(countrySelectModalRef)) return;
    closeCountryModal();
  }

  function handleCountrySelection(country: string, code: string) {
    dispatch("countrySelected", {
        country, 
        code, 
        srcCountrySelected: isSrcCountryOptionSelected
    });
    closeCountryModal();
  }

  function searchCountry(searchText: string) {
    countries = [...COUNTRIES];

    if (searchText === "") return;

    const foundCountries = countries.filter(country => country.country.toLowerCase().includes(searchText));
    countries = [...foundCountries];
  }

  function searchDebounce(callbackFunc: any, delay: number = 500) {
    let timeout: any;

    return (...args: any[]) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        callbackFunc(...args);
      }, delay);
    };
  }

  const updateDebounceSearch = searchDebounce((searchText: string) => {
    searchCountry(searchText);
  });

  function handleCountrySearch() {
    updateDebounceSearch(countrySearchInput.trim());
  }

  function closeCountryModal() {
    dispatch("closeModal", true);
  }

  afterUpdate(() => {
    initialMount();
  });

  async function initialMount() {
    let timeout;

    clearTimeout(timeout);
    timeout = setTimeout(() => {
        searchCountryInputRef?.focus();
    }, 50);
    countryListRef.style.height = `calc(100% - ${modalTopRef.offsetHeight}px)`;
  }
</script>

<svelte:window on:click={handleWindowClick} on:keyup={handleWindowKeyup} />

<div
  class="fixed top-0 left-0 h-screen w-full px-5 md:px-10 lg:px-20"
  style="background-color: rgba(0, 0, 0, 0.5);"
>
  <div
    transition:scale={{
      duration: 500,
      opacity: 0.5,
      start: 0.5,
      easing: quintOut,
    }}
    bind:this={countrySelectModalRef}
    class="absolute top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] w-[95%] sm:max-w-[800px] h-[70vh] bg-stone-800 shadow-md rounded-md"
  >
    <div class="w-full h-full">
      <div bind:this={modalTopRef} class="flex flex-col gap-y-3 p-3">
        <div class="flex justify-end">
          <button
            on:click={closeCountryModal}
            type="button"
            class="flex items-center gap-x-1 text-rose-400 hover:text-rose-500 transition-colors duration-200 ease-linear"
          >
            <Icon icon="ic:round-close" />
            Close
          </button>
        </div>
        <div class="w-full">
          <input
            bind:this={searchCountryInputRef}
            bind:value={countrySearchInput}
            on:keyup={handleCountrySearch}
            type="text"
            placeholder="Search country..."
            class="w-full p-3 bg-stone-700 focus:outline-none rounded-md"
          />
        </div>
      </div>

      <div
        bind:this={countryListRef}
        class="grid grid-cols-4 w-full h-full overflow-y-auto px-3 content-start"
      >
        {#each countries as country}
          <button
            on:click={() =>
              handleCountrySelection(country.country, country.code)}
            type="button"
            class="py-2 px-3 rounded-md hover:bg-stone-700"
            >{country.country}</button
          >
        {/each}
      </div>
    </div>
  </div>
</div>
