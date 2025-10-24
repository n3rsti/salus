<template>
    <main class="flex flex-col justify-center items-center content-center p-4">
        <h2 class="text-green-500 font-semibold text-4xl text-center">
            Login in to salus
        </h2>
        <form
            class="rounded-xl border-3 border-green-500 bg-primary-light text-green-700 mt-8 p-4 w-4/6"
        >
            <label
                class="input validator bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 w-full"
            >
                <svg
                    class="h-[1em] opacity-50"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                >
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                        <path
                            d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"
                        ></path>
                    </g>
                </svg>
                <input type="email" placeholder="mail@site.com" required />
            </label>
            <div class="validator-hint hidden">Enter valid email address</div>

            <label
                class="input validator bg-amber-50 border-2 border-primary-dark rounded-xl focus-within:border-green-500 mt-4 w-full"
            >
                <svg
                    class="h-[1em] opacity-50"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                >
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2.5"
                        fill="none"
                        stroke="currentColor"
                    >
                        <path
                            d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
                        ></path>
                        <circle
                            cx="16.5"
                            cy="7.5"
                            r=".5"
                            fill="currentColor"
                        ></circle>
                    </g>
                </svg>
                <input
                    type="password"
                    required
                    placeholder="Password"
                    minlength="8"
                    pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                    title="Must be more than 8 characters, including number, lowercase letter, uppercase letter"
                />
            </label>
            <p class="validator-hint hidden">
                Must be more than 8 characters, including
                <br />At least one number <br />At least one lowercase letter
                <br />At least one uppercase letter
            </p>

            <AppButton
                class="w-full shadow-sm border-t-transparent text-white mt-4"
                :color="'green'"
            >
                <svg
                    aria-label="Email icon"
                    width="16"
                    height="16"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                >
                    <g
                        stroke-linejoin="round"
                        stroke-linecap="round"
                        stroke-width="2"
                        fill="none"
                        stroke="white"
                    >
                        <rect width="20" height="16" x="2" y="4" rx="2"></rect>
                        <path
                            d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"
                        ></path>
                    </g>
                </svg>
                <span class="ml-1">Login with Email</span>
            </AppButton>

            <p class="mt-4">
                Not yet a user?<br />
                <a
                    class="text-green-900 underline hover:cursor-pointer hover:text-green-600"
                    >Sing up</a
                >
            </p>

            <button
                class="btn bg-white text-black border-[#2F2F2F] w-full mt-10"
            >
                <svg
                    aria-label="Microsoft logo"
                    width="16"
                    height="16"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 512 512"
                >
                    <path d="M96 96H247V247H96" fill="#f24f23"></path>
                    <path d="M265 96V247H416V96" fill="#7eba03"></path>
                    <path d="M96 265H247V416H96" fill="#3ca4ef"></path>
                    <path d="M265 265H416V416H265" fill="#f9ba00"></path>
                </svg>
                Login with Microsoft
            </button>
            <button
                class="btn bg-white text-black border-[#e5e5e5] w-full mt-4"
            >
                <svg
                    aria-label="Google logo"
                    width="16"
                    height="16"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 512 512"
                >
                    <g>
                        <path d="m0 0H512V512H0" fill="#fff"></path>
                        <path
                            fill="#34a853"
                            d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"
                        ></path>
                        <path
                            fill="#4285f4"
                            d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"
                        ></path>
                        <path
                            fill="#fbbc02"
                            d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"
                        ></path>
                        <path
                            fill="#ea4335"
                            d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"
                        ></path>
                    </g>
                </svg>
                Login with Google
            </button>
            <button
                class="btn bg-white text-black border-[#e17d00] w-full mt-4"
            >
                <svg
                    aria-label="Amazon logo"
                    width="16"
                    height="16"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 16 16"
                >
                    <g fill="black">
                        <path
                            d="M14.463 13.831c-1.753 1.294-4.291 1.981-6.478 1.981-3.066 0-5.825-1.131-7.912-3.019-.163-.147-.019-.35.178-.234 2.253 1.313 5.041 2.1 7.919 2.1 1.941 0 4.075-.403 6.041-1.238.294-.125.544.197.253.409z"
                        ></path>
                        <path
                            d="M15.191 13c-.225-.287-1.481-.137-2.047-.069-.172.019-.197-.128-.044-.238 1.003-.703 2.647-.5 2.838-.266.194.238-.05 1.884-.991 2.672-.144.122-.281.056-.219-.103.216-.528.688-1.709.463-1.997zM11.053 11.838l.003.003c.387-.341 1.084-.95 1.478-1.278.156-.125.128-.334.006-.509-.353-.488-.728-.884-.728-1.784v-3c0-1.272.088-2.438-.847-3.313-.738-.706-1.963-.956-2.9-.956-1.831 0-3.875.684-4.303 2.947-.047.241.131.369.287.403l1.866.203c.175-.009.3-.181.334-.356.159-.778.813-1.156 1.547-1.156.397 0 .847.144 1.081.5.269.397.234.938.234 1.397v.25c-1.116.125-2.575.206-3.619.666-1.206.522-2.053 1.584-2.053 3.147 0 2 1.259 3 2.881 3 1.369 0 2.116-.322 3.172-1.403.35.506.463.753 1.103 1.284a.395.395 0 0 0 .456-.044zm-1.94-4.694c0 .75.019 1.375-.359 2.041-.306.544-.791.875-1.331.875-.737 0-1.169-.563-1.169-1.394 0-1.641 1.472-1.938 2.863-1.938v.416z"
                        ></path>
                    </g>
                </svg>
                Login with Amazon
            </button>
        </form>
    </main>
</template>
<script setup lang="ts">
definePageMeta({
    layout: "authentication",
});
</script>
