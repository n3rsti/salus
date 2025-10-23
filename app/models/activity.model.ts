export class Activity {
    constructor(
        public id: number,
        public name: string,
        public duration: number,
        public description: string,
        public difficulty: number,
        public rating: number,
        public image: string,
    ) {}
}

export class ActivityBuilder {
    private id!: number;
    private name!: string;
    private duration!: number;
    private description!: string;
    private difficulty!: number;
    private rating!: number;
    private image!: string;

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

    setDifficulty(difficulty: number): this {
        this.difficulty = difficulty;
        return this;
    }

    setRating(rating: number): this {
        this.rating = rating;
        return this;
    }

    setImage(image: string): this {
        this.image = image;
        return this;
    }

    build(): Activity {
        return new Activity(
            this.id,
            this.name,
            this.duration,
            this.description,
            this.difficulty,
            this.rating,
            this.image,
        );
    }
}
