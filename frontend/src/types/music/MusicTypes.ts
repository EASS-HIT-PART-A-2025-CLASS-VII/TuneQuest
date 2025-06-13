export interface BaseAlbum {
  id: string;
  name: string;
  images: Array<{ url: string }>;
}

export interface BaseTrack {
  id: string;
  name: string;
}

export interface FullTrack extends BaseTrack {
    album: {
      id: string;
      name: string;
      images: Array<{ url: string }>;
    };
    artists: Array<{ id: string; name: string }>;
    duration_ms: number;
    popularity: number;
  }
  
export interface Artist {
  id: string;
  name: string;
  genres: string[];
  followers: { total: number };
  popularity: number;
  images: Array<{ url: string }>;
}


export interface FullAlbum extends BaseAlbum {
  album_type: string;
  release_date: string;
  release_date_precision: string;
  popularity: number;
  artists: Array<{ id: string; name: string }>;
  tracks: {
    items: Array<{ id: string; name: string }>;
  };
}

export interface SearchResults {
  tracks: Array<FullTrack>;
  albums: Array<FullAlbum>;
  artists: Array<Artist>;
}

export interface SearchResult {
  tracks: { id: string; name: string; artists: { id: string; name: string }[] }[];
  albums: { id: string; name: string; artists: { id: string; name: string }[] }[];
  artists: { id: string; name: string }[];
} 