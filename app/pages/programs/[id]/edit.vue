<template>
    <AppProgramForm
        :initial-data="program"
        @submit="submitForm"
        @delete="deleteProgram"
    ></AppProgramForm>
</template>

<script setup lang="ts">
import type { Program } from "~/models/program.model";
import type { ProgramDay } from "~/models/program_day.model";

const route = useRoute();

const emptyProgram: Program = {
    name: "",
    description: "",
    duration_days: 1,
    image_url: "",
    language: "",
};

const { data: program } = await useFetch<Program>(
    `/api/programs/${route.params.id}`,
);

if (!program.value) {
    throw createError({
        statusCode: 404,
        statusMessage: "Program Not Found",
    });
}

async function createDays(program: Program, program_id: number) {
    if (!program.days) return;

    for (const day of program.days) {
        const newDay: ProgramDay = {
            description: day.description,
            day_number: day.day_number,
            program_id,
        };
        await createDay(newDay, day);
    }
}

async function createDay(newDay: ProgramDay, originalDay: ProgramDay) {
    const data = await $fetch<ProgramDay>("/api/programs/days", {
        method: "POST",
        body: newDay,
    });

    if (data?.id) {
        await linkActivities(originalDay, data.id);
    }
}

async function linkActivities(day: ProgramDay, program_day_id: number) {
    if (!day.activities) return;

    for (const activity of day.activities) {
        if (activity.id) {
            await linkActivity(program_day_id, activity.id);
        }
    }
}

async function linkActivity(program_day_id: number, activity_id: number) {
    await $fetch(
        `/api/programs/days/${program_day_id}/activities/${activity_id}/`,
        {
            method: "POST",
        },
    );
}

async function submitForm(program: Program) {
    try {
        const data = await $fetch<Program>("/api/programs/", {
            method: "PUT",
            body: program,
        });

        if (data?.id) {
            await createDays(program, data.id);
            await navigateTo(`/programs/${data.id}`);
        }
    } catch (error) {
        console.error("Failed to create program:", error);
    }
}

async function deleteProgram() {
    try {
        await $fetch(`/api/programs/${route.params.id}`, {
            method: "DELETE",
        });
        await navigateTo("/programs");
    } catch (error) {
        console.error("Failed to delete program:", error);
    }
}
</script>
