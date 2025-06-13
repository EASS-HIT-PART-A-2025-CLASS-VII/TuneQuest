export interface RecommendationItem {
    id: string;
    name: string;
    type: string;
    image: string;
    url: string;
}

export interface AiButtonProps {
    readonly type: string;
    readonly name: string;
}

export interface Message {
    id: string;
    sender: "user" | "ai";
    content: string | {
      tracks: any[];
      artists: any[];
      albums: any[];
    };
}

