<script lang="ts">
  import { onMount, beforeUpdate, afterUpdate } from "svelte";
  import Icon from "@iconify/svelte";
  import { toasts, ToastContainer, FlatToast } from "svelte-toasts";
  import tippy from "tippy.js";
  import "tippy.js/dist/tippy.css"; // optional for styling
  import CountrySelectionModal from "./CountrySelectionModal.svelte";
  import "../../css/home/TranslatorCard.css";
  import axios from "axios";
  import { API_URL } from "../ts/API";
  import { showToast } from "../ts/toast";

  let srcTextAreaRef: any,
    srcLangMicRef: any,
    srcLangCopyRef: any,
    destLangMicRef: any,
    destLangCopyRef: any,
    swapBtnRef: any;
  let toggleBigScreenMode: boolean = true;
  let srcText: string = "",
    translatedText: string = "";
  let isTranslating: boolean = false;

  let isSrcCountryOptionSelected: boolean = false,
    showCountries: boolean = false;

  let srcSelectedLanguage = {
    country: "English",
    code: "en",
  };
  let destSelectedLanguage = {
    country: "Bangla",
    code: "bn",
  };

  function handleCountryOptionSelection(isSrcSelected: boolean) {
    isSrcCountryOptionSelected = isSrcSelected;
    showCountries = true;

    document.body.classList.add("overflow-y-hidden");
  }

  function handleCountrySelection(event: any) {
    const { country, code, srcCountrySelected } = event.detail;

    if (srcCountrySelected) {
      srcSelectedLanguage = {
        country: country,
        code: code,
      };
    } else {
      destSelectedLanguage = {
        country: country,
        code: code,
      };
    }

    translateTextToAnotherLanguage(srcText.trim());
  }

  function closeCountryModal(event: any) {
    showCountries = !event.detail;
    document.body.classList.remove("overflow-y-hidden");
  }

  async function translateTextToAnotherLanguage(text: string) {
    isTranslating = true;

    if (text === "") {
      isTranslating = false;
      translatedText = "";
      return;
    }

    let formData = new FormData();
    formData.append("text", text);
    formData.append("srcLang", srcSelectedLanguage.code);
    formData.append("destLang", destSelectedLanguage.code);

    await axios
      .post(`${API_URL}/translate/`, formData, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((res) => {
        const { error, status, text } = res.data;

        if (error && status === 400) {
          showToast(toasts, "error", "Error", "Failed to translate!");
        } else if (!error && status === 200) {
          translatedText = text;
        }
      })
      .catch((err) => {
        showToast(toasts, "error", "Error", "Something went wrong!");
      });

    isTranslating = false;
  }

  function handleSwapLanguage() {
    // Swap text
    [srcText, translatedText] = [translatedText, srcText];
    // Swap language
    [srcSelectedLanguage, destSelectedLanguage] = [
      destSelectedLanguage,
      srcSelectedLanguage,
    ];
  }

  function handleTextToSpeech(isSrc: boolean) {
    let text = "",
      countryCode = "en";

    if (isSrc) {
      text = srcText.trim();
      countryCode = srcSelectedLanguage.code;
    } else {
      text = translatedText.trim();
      countryCode = destSelectedLanguage.code;
    }

    if (text === "") return;

    const message = new SpeechSynthesisUtterance(text);
    message.lang = countryCode;
    message.pitch = 1;
    message.rate = 1;
    window.speechSynthesis.speak(message);
  }

  // Copy text to clipboard
  function handleCopyText(isSrc: boolean) {
    let text = "";

    if (isSrc) {
      text = srcText.trim();
    } else {
      text = translatedText.trim();
    }

    if (text === "") return;

    navigator.clipboard
      .writeText(text)
      .then(() => {
        showToast(toasts, "success", "Success", "Text coppied successfully.");
      })
      .catch((err) => {
        showToast(toasts, "error", "Error", "Failed to copy text!");
      });
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

  const updateDebounceSearch = searchDebounce((text: string) => {
    translateTextToAnotherLanguage(text);
  });

  function handleTranslateText(e: any) {
    if (e.key === "Escape") return;

    updateDebounceSearch(srcText.trim());
  }

  function handleWindowResize() {
    if (window.innerWidth <= 640) {
      toggleBigScreenMode = false;
    } else {
      toggleBigScreenMode = true;
    }
  }

  beforeUpdate(() => {
    handleWindowResize();
  });

  afterUpdate(() => {
    initialMount();
  });

  function initialMount() {
    tippy(srcLangMicRef, {
      content: "Listen",
      placement: "bottom",
    });
    tippy(srcLangCopyRef, {
      content: "Copy",
      placement: "bottom",
    });
    tippy(destLangMicRef, {
      content: "Listen",
      placement: "bottom",
    });
    tippy(destLangCopyRef, {
      content: "Copy",
      placement: "bottom",
    });
    tippy(swapBtnRef, {
      content: "Swap",
      placement: "bottom",
    });

    srcTextAreaRef?.focus();
  }
</script>

<svelte:window on:resize={handleWindowResize} />

<ToastContainer placement="bottom-right" let:data>
  <FlatToast {data} />
  <!-- Provider template for your toasts -->
</ToastContainer>

{#if showCountries}
  <CountrySelectionModal
    {isSrcCountryOptionSelected}
    on:countrySelected={handleCountrySelection}
    on:closeModal={closeCountryModal}
  />
{/if}

<div class="w-full px-5 md:px-10 lg:px-20 my-10">
  <div
    class="w-auto max-w-screen-2xl mx-auto p-3 rounded-md shadow-md bg__dark1"
  >
    <h1 class="text-xl md:text-2xl text-center mb-3.5 font-semibold">
      Global Translator
    </h1>

    <div class="w-full bg-stone-800 rounded-t-md">
      <div class="grid grid-cols-1 sm:grid-cols-2 items-center justify-between">
        <div class="w-full h-[250px] sm:h-[350px] flex flex-col">
          <textarea
            on:keyup={handleTranslateText}
            bind:this={srcTextAreaRef}
            bind:value={srcText}
            class="w-full h-full p-5 focus:outline-none bg-transparent resize-none"
            placeholder="Enter text here..."
          />

          {#if !toggleBigScreenMode}
            <div
              class="px-5 py-3 flex flex-1 items-center justify-between gap-x-5 border-t border-stone-600"
            >
              <div class="flex items-center gap-x-5">
                <div>
                  <button
                    on:click={() => handleTextToSpeech(true)}
                    bind:this={srcLangMicRef}
                    type="button"
                    class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                  >
                    <Icon class="text-xl" icon="iconoir:sound-high" />
                  </button>
                </div>
                <div>
                  <button
                    on:click={() => handleCopyText(true)}
                    bind:this={srcLangCopyRef}
                    type="button"
                    class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                  >
                    <Icon class="text-xl" icon="ic:outline-content-copy" />
                  </button>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <button
                  on:click={() => handleCountryOptionSelection(true)}
                  type="button"
                  class="flex items-center justify-between gap-x-10 rounded-md bg-stone-700 hover:bg-stone-600 px-3 py-2 transition-colors duration-200 ease-linear"
                >
                  <p>{srcSelectedLanguage.country}</p>
                  <Icon
                    class="text-xl"
                    icon="material-symbols:keyboard-arrow-down-rounded"
                  />
                </button>
              </div>
            </div>
          {/if}
        </div>
        <div
          class="w-full h-[250px] sm:h-[350px] border-t sm:border-t-0 sm:border-l border-stone-600 flex flex-col"
        >
          <div class="w-full h-full p-5 overflow-y-auto">
            {#if isTranslating}
              <div class="flex items-center justify-center w-full h-full">
                <Icon
                  icon="eos-icons:bubble-loading"
                  class="text-3xl sm:text-5xl"
                />
              </div>
            {:else}
              {translatedText}
            {/if}
          </div>

          {#if !toggleBigScreenMode}
            <div
              class="px-5 py-3 flex flex-1 items-center justify-between gap-x-5 border-t border-stone-600"
            >
              <div class="flex items-center gap-x-5">
                <div>
                  <button
                    on:click={() => handleTextToSpeech(false)}
                    bind:this={destLangMicRef}
                    type="button"
                    class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                  >
                    <Icon class="text-xl" icon="iconoir:sound-high" />
                  </button>
                </div>
                <div>
                  <button
                    on:click={() => handleCopyText(false)}
                    bind:this={destLangCopyRef}
                    type="button"
                    class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                  >
                    <Icon class="text-xl" icon="ic:outline-content-copy" />
                  </button>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <button
                  on:click={() => handleCountryOptionSelection(false)}
                  type="button"
                  class="flex items-center justify-between gap-x-10 rounded-md bg-stone-700 hover:bg-stone-600 px-3 py-2 transition-colors duration-200 ease-linear"
                >
                  <p>{destSelectedLanguage.country}</p>
                  <Icon
                    class="text-xl"
                    icon="material-symbols:keyboard-arrow-down-rounded"
                  />
                </button>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
    {#if toggleBigScreenMode}
      <div class="w-full bg-stone-800 rounded-b-md border-t border-stone-600">
        <div id="translate__card" class="grid items-center justify-between">
          <div class="p-5 flex flex-1 items-center justify-between gap-x-5">
            <div class="flex items-center gap-x-5">
              <div>
                <button
                  bind:this={srcLangMicRef}
                  on:click={() => handleTextToSpeech(true)}
                  type="button"
                  class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                >
                  <Icon class="text-xl" icon="iconoir:sound-high" />
                </button>
              </div>
              <div>
                <button
                  on:click={() => handleCopyText(true)}
                  bind:this={srcLangCopyRef}
                  type="button"
                  class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                >
                  <Icon class="text-xl" icon="ic:outline-content-copy" />
                </button>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <button
                on:click={() => handleCountryOptionSelection(true)}
                type="button"
                class="flex items-center justify-between gap-x-10 rounded-md bg-stone-700 hover:bg-stone-600 px-3 py-2 transition-colors duration-200 ease-linear"
              >
                <p>{srcSelectedLanguage.country}</p>
                <Icon
                  class="text-xl"
                  icon="material-symbols:keyboard-arrow-down-rounded"
                />
              </button>
            </div>
          </div>
          <div class="flex justify-center">
            <button
              on:click={handleSwapLanguage}
              bind:this={swapBtnRef}
              type="button"
              class="py-1 px-2 hover:bg-stone-700 rounded-md transition-colors duration-200 ease-linear"
            >
              <Icon
                class="text-xl"
                icon="material-symbols:swap-horiz-rounded"
              />
            </button>
          </div>
          <div class="p-5 flex items-center justify-between gap-x-5">
            <div class="flex items-center justify-between">
              <button
                on:click={() => handleCountryOptionSelection(false)}
                type="button"
                class="flex items-center justify-between gap-x-10 rounded-md bg-stone-700 hover:bg-stone-600 px-3 py-2 transition-colors duration-200 ease-linear"
              >
                <p>{destSelectedLanguage.country}</p>
                <Icon
                  class="text-xl"
                  icon="material-symbols:keyboard-arrow-down-rounded"
                />
              </button>
            </div>
            <div class="flex items-center gap-x-5">
              <div>
                <button
                  on:click={() => handleTextToSpeech(false)}
                  bind:this={destLangMicRef}
                  type="button"
                  class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                >
                  <Icon class="text-xl" icon="iconoir:sound-high" />
                </button>
              </div>
              <div>
                <button
                  on:click={() => handleCopyText(false)}
                  bind:this={destLangCopyRef}
                  type="button"
                  class="hover:text-sky-500 transition-colors duration-200 ease-linear"
                >
                  <Icon class="text-xl" icon="ic:outline-content-copy" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
