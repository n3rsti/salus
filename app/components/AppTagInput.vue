<template>
    <Popover v-model:open="open">
        <ListboxRoot v-model="internalValue" highlight-on-hover multiple>
            <PopoverAnchor class="inline-flex w-full">
                <TagsInput v-model="internalValue" class="w-full">
                    <TagsInputItem
                        v-for="tag in internalValue"
                        :key="tag"
                        :value="tag"
                        class="text-white"
                        :class="TagColors[tag]"
                    >
                        <span class="text-xs font-semibold p-2">{{
                            TagNames[tag]
                        }}</span>
                        <TagsInputItemDelete />
                    </TagsInputItem>

                    <ListboxFilter v-model="searchTerm" as-child>
                        <TagsInputInput
                            placeholder="Tags..."
                            @keydown.enter.prevent
                            @keydown.down="open = true"
                        />
                    </ListboxFilter>

                    <PopoverTrigger as-child>
                        <Button
                            size="icon-sm"
                            variant="ghost"
                            class="order-last self-start ml-auto"
                        >
                            <ChevronDown class="size-3.5" />
                        </Button>
                    </PopoverTrigger>
                </TagsInput>
            </PopoverAnchor>

            <PopoverContent class="p-1" @open-auto-focus.prevent>
                <ListboxContent
                    class="scroll-py-1 overflow-x-hidden overflow-y-auto empty:after:content-['No_options'] empty:p-1 empty:after:block"
                    tabindex="0"
                >
                    <ListboxItem
                        v-for="item in filteredTags"
                        :key="item.value"
                        :value="item.value"
                        class="data-[highlighted]:bg-accent data-[highlighted]:text-accent-foreground [&_svg:not([class*='text-'])]:text-muted-foreground relative flex cursor-default items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-hidden select-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"
                        @select="
                            () => {
                                searchTerm = '';
                            }
                        "
                    >
                        <span>{{ item.label }}</span>

                        <ListboxItemIndicator
                            class="ml-auto inline-flex items-center justify-center"
                        >
                            <CheckIcon />
                        </ListboxItemIndicator>
                    </ListboxItem>
                </ListboxContent>
            </PopoverContent>
        </ListboxRoot>
    </Popover>
</template>

<script setup lang="ts">
import { CheckIcon, ChevronDown } from "lucide-vue-next";
import {
    ListboxContent,
    ListboxFilter,
    ListboxItem,
    ListboxItemIndicator,
    ListboxRoot,
    useFilter,
} from "reka-ui";
import { computed, ref, watch } from "vue";
import { Button } from "@/components/ui/button";
import {
    Popover,
    PopoverAnchor,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import {
    TagsInput,
    TagsInputInput,
    TagsInputItem,
    TagsInputItemDelete,
} from "@/components/ui/tags-input";
import { Tag, TagColors, TagNames } from "~/constants/tags";

const props = defineProps<{
    selectedTags?: Tag[];
}>();

const emit = defineEmits<{
    updateTags: [tags: Tag[]];
}>();

const internalValue = computed<Tag[]>({
    get: () => props.selectedTags ?? [],
    set: (value) => emit("updateTags", value),
});

const tagsValues = (
    Object.values(Tag).filter((v): v is Tag => typeof v === "number") as Tag[]
).map((tag) => ({
    value: tag,
    label: TagNames[tag],
}));

const searchTerm = ref("");
const open = ref(false);

const { contains } = useFilter({ sensitivity: "base" });

const filteredTags = computed(() =>
    searchTerm.value === ""
        ? tagsValues
        : tagsValues.filter((option) =>
              contains(option.label, searchTerm.value),
          ),
);

watch(searchTerm, (v) => {
    if (v) open.value = true;
});
</script>
