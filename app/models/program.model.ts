export class Program {
    constructor(
        public id: number,
        public name: string,
        public duration: number,
        public description: string,
        public language: string,
        public image: string,
        public progress: number,
        public rating: number,
    ) {}
}

export class ProgramBuilder {
    private id!: number;
    private name!: string;
    private duration!: number;
    private description!: string;
    private language!: string;
    private image!: string;
    private progress!: number;
    private rating!: number;

    setId(id: number): this {
        this.id = id;
        return this;
    }

    setName(name: string): this {
        this.name = name;
        return this;
    }

    setDuration(duration: number): this {
        this.duration = duration;
        return this;
    }

    setDescription(description: string): this {
        this.description = description;
        return this;
    }

    setLanguage(language: string): this {
        this.language = language;
        return this;
    }

    setImage(image: string): this {
        this.image = image;
        return this;
    }

    setProgress(progress: number): this {
        this.progress = progress;
        return this;
    }

    setRating(rating: number): this {
        this.rating = rating;
        return this;
    }

    build(): Program {
        return new Program(
            this.id,
            this.name,
            this.duration,
            this.description,
            this.language,
            this.image,
            this.progress,
            this.rating,
        );
    }
}
