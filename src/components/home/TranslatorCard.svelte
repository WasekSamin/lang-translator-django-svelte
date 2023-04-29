<script lang="ts">
    import {onMount} from "svelte";
    import Icon from '@iconify/svelte';
    import tippy from "tippy.js";
    import "tippy.js/dist/tippy.css"; // optional for styling
    import { COUNTRIES } from "../ts/country";
    import "../../css/home/TranslatorCard.css";

    let srcLangMicRef: any, srcLangCopyRef: any;
    let distLangMicRef: any, distLangCopyRef: any;
    let swapBtnRef: any;

    let selectedLanguage = {
        lang: "English",
        code: "en"
    };

    onMount(() => {
        initialMount();
    })

    function initialMount() {
        tippy(srcLangMicRef, {
            content: "Listen",
            placement: "bottom"
        });
        tippy(srcLangCopyRef, {
            content: "Copy",
            placement: "bottom"
        });
        tippy(distLangMicRef, {
            content: "Listen",
            placement: "bottom"
        });
        tippy(distLangCopyRef, {
            content: "Copy",
            placement: "bottom"
        });
        tippy(swapBtnRef, {
            content: "Swap",
            placement: "bottom"
        });
    }
</script>

<div class="w-full max-w-screen-2xl px-5 md:px-10 lg:px-20 my-10">
    <div class="w-auto max-w-screen-2xl mx-auto p-3 rounded-md shadow-md bg__dark1">
        <div class="w-full bg-stone-800 rounded-t-md">
            <div class="grid grid-cols-2 items-center justify-between">
                <textarea class="h-[350px] p-5 focus:outline-none bg-transparent resize-none">Left</textarea>
                <div class="p-5 h-[350px] border-l border-stone-600 overflow-y-auto">
                    Right
                </div>
            </div>
        </div>
        <div class="w-full bg-stone-800 rounded-b-md border-t border-stone-600">
            <div id="translate__card" class="grid items-center justify-between">
                <div class="p-5 flex flex-1 items-center justify-between gap-x-5">
                    <div class="flex items-center gap-x-5">
                        <div>
                            <button bind:this={srcLangMicRef} type="button" class="hover:text-sky-500 transition-colors duration-200 ease-linear">
                                <Icon class="text-xl" icon="iconoir:sound-high" />
                            </button>
                        </div>
                        <div>
                            <button bind:this={srcLangCopyRef} type="button" class="hover:text-sky-500 transition-colors duration-200 ease-linear">
                                <Icon class="text-xl" icon="ic:outline-content-copy" />
                            </button>
                        </div>
                    </div>
                    <div class="flex items-center justify-between">
                        <button type="button" class="flex items-center justify-between gap-x-10 rounded-md bg-stone-700 hover:bg-stone-600 px-3 py-2 transition-colors duration-200 ease-linear">
                            <p>{selectedLanguage.lang}</p>
                            <Icon class="text-xl" icon="material-symbols:keyboard-arrow-down-rounded" />
                        </button>
                    </div>
                </div>
                <div class="flex justify-center">
                    <button bind:this={swapBtnRef} type="button" class="py-1 px-2 hover:bg-stone-700 rounded-md transition-colors duration-200 ease-linear">
                        <Icon class="text-xl" icon="material-symbols:swap-horiz-rounded" />
                    </button>
                </div>
                <div class="p-5 flex items-center justify-between gap-x-5">
                    <div class="flex items-center justify-between">
                        <button type="button" class="flex items-center justify-between gap-x-10 rounded-md bg-stone-700 hover:bg-stone-600 px-3 py-2 transition-colors duration-200 ease-linear">
                            <p>{selectedLanguage.lang}</p>
                            <Icon class="text-xl" icon="material-symbols:keyboard-arrow-down-rounded" />
                        </button>
                    </div>
                    <div class="flex items-center gap-x-5">
                        <div>
                            <button bind:this={srcLangMicRef} type="button" class="hover:text-sky-500 transition-colors duration-200 ease-linear">
                                <Icon class="text-xl" icon="iconoir:sound-high" />
                            </button>
                        </div>
                        <div>
                            <button bind:this={srcLangCopyRef} type="button" class="hover:text-sky-500 transition-colors duration-200 ease-linear">
                                <Icon class="text-xl" icon="ic:outline-content-copy" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>