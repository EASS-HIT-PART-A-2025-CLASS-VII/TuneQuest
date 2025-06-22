import { render, screen } from "@testing-library/react";
import { test, expect, describe, vi } from "vitest";
import { MemoryRouter } from 'react-router-dom';

import { TrackCard, AlbumCard, ArtistCard, NonImageTrackCard, CompactAlbumCard } from "../../components/features/Cards";

vi.mock('../../components/common/Cards.module.css', () => ({ default: {} }));


describe('TrackCard', () => {
  const mockTrack = {
    id: 'track123',
    name: 'Test Track Name',
    album: {
      images: [{ url: 'http://example.com/track-image.jpg' }]
    },
    artists: [{ name: 'Artist A' }, { name: 'Artist B' }]
  };

  test('renders TrackCard with correct track information', () => {
    render(
      <MemoryRouter>
        <TrackCard track={mockTrack} />
      </MemoryRouter>
    );

    expect(screen.getByText('Test Track Name')).toBeInTheDocument();
    expect(screen.getByText('Artist A, Artist B')).toBeInTheDocument();

    const image = screen.getByAltText('Test Track Name');
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute('src', 'http://example.com/track-image.jpg');

    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/track/track123');
  });

  test('renders TrackCard correctly when track has no artists', () => {
    const trackNoArtists = { ...mockTrack, artists: [] };
    render(
      <MemoryRouter>
        <TrackCard track={trackNoArtists} />
      </MemoryRouter>
    );
    expect(screen.getByText('Test Track Name')).toBeInTheDocument();
    expect(screen.queryByText('Artist A')).not.toBeInTheDocument();
    expect(screen.queryByText('Artist B')).not.toBeInTheDocument();
  });

  test('handles missing album images gracefully', () => {
    const trackNoImage = { ...mockTrack, album: { images: [] } };
    render(
      <MemoryRouter>
        <TrackCard track={trackNoImage} />
      </MemoryRouter>
    );
    const image = screen.getByAltText('Test Track Name');
    expect(image).toBeInTheDocument();
    expect(image).not.toHaveAttribute('src');
  });
});


describe('AlbumCard', () => {
  const mockAlbumFullDate = {
    id: 'album456',
    name: 'Test Album Full Date',
    images: [{ url: 'http://example.com/album-image.jpg' }],
    artists: [{ name: 'Album Artist C' }],
    release_date: '2023-05-10',
    release_date_precision: 'day'
  };

  const mockAlbumYearOnly = {
    id: 'album789',
    name: 'Test Album Year Only',
    images: [{ url: 'http://example.com/album-year-image.jpg' }],
    artists: [{ name: 'Album Artist D' }],
    release_date: '2022',
    release_date_precision: 'year'
  };

  test('renders AlbumCard with full date precision', () => {
    render(
      <MemoryRouter>
        <AlbumCard album={mockAlbumFullDate} />
      </MemoryRouter>
    );

    expect(screen.getByText('Test Album Full Date')).toBeInTheDocument();
    expect(screen.getByText('Album Artist C')).toBeInTheDocument();
    expect(screen.getByText('2023')).toBeInTheDocument();
    expect(screen.getByAltText('Test Album Full Date')).toHaveAttribute('src', 'http://example.com/album-image.jpg');
    expect(screen.getByRole('link')).toHaveAttribute('href', '/album/album456');
  });

  test('renders AlbumCard with year only precision', () => {
    render(
      <MemoryRouter>
        <AlbumCard album={mockAlbumYearOnly} />
      </MemoryRouter>
    );

    expect(screen.getByText('Test Album Year Only')).toBeInTheDocument();
    expect(screen.getByText('Album Artist D')).toBeInTheDocument();
    expect(screen.getByText('2022')).toBeInTheDocument();
    expect(screen.getByAltText('Test Album Year Only')).toHaveAttribute('src', 'http://example.com/album-year-image.jpg');
    expect(screen.getByRole('link')).toHaveAttribute('href', '/album/album789');
  });

  test('handles missing album images gracefully', () => {
    const albumNoImage = { ...mockAlbumFullDate, images: [] };
    render(
      <MemoryRouter>
        <AlbumCard album={albumNoImage} />
      </MemoryRouter>
    );
    const image = screen.getByAltText('Test Album Full Date');
    expect(image).toBeInTheDocument();
    expect(image).not.toHaveAttribute('src');
  });
});


describe('ArtistCard', () => {
  const mockArtistWithImage = {
    id: 'artist789',
    name: 'Test Artist Name',
    images: [{ url: 'http://example.com/artist-image.jpg' }]
  };

  const mockArtistNoImage = {
    id: 'artist000',
    name: 'Artist Without Image',
    images: []
  };

  test('renders ArtistCard with image', () => {
    render(
      <MemoryRouter>
        <ArtistCard artist={mockArtistWithImage} />
      </MemoryRouter>
    );

    expect(screen.getByText('Test Artist Name')).toBeInTheDocument();
    const image = screen.getByAltText('Test Artist Name');
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute('src', 'http://example.com/artist-image.jpg');
    expect(screen.getByRole('link')).toHaveAttribute('href', '/artist/artist789');
  });

  test('renders ArtistCard with default image when no image is provided', () => {
    render(
      <MemoryRouter>
        <ArtistCard artist={mockArtistNoImage} />
      </MemoryRouter>
    );

    expect(screen.getByText('Artist Without Image')).toBeInTheDocument();
    const image = screen.getByAltText('Artist Without Image');
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute('src', '/default-artist.png');
  });
});


describe('NonImageTrackCard', () => {
    const mockTrackWithoutImage = {
        id: 'track123',
        name: 'Test Track Name',
        track_number: 1,
        artists: [{ name: 'Artist A' }, { name: 'Artist B' }]
    }

    test('renders TrackCard without image', () => {
        render(
            <MemoryRouter>
                <NonImageTrackCard track={mockTrackWithoutImage} />
            </MemoryRouter>
        );
        expect(screen.getByText('Test Track Name')).toBeInTheDocument();
        expect(screen.getByText('Artist A, Artist B')).toBeInTheDocument();
        const link = screen.getByRole('link')
        expect(link).toHaveAttribute('href','/track/track123')
    })

    test('renders TrackCard correctly when track has no artists', () => {
        const trackNoArtists = { ...mockTrackWithoutImage, artists: [] };
        render(
          <MemoryRouter>
            <NonImageTrackCard track={trackNoArtists} />
          </MemoryRouter>
        );
        expect(screen.getByText('Test Track Name')).toBeInTheDocument();
        expect(screen.queryByText('Artist A')).not.toBeInTheDocument();
        expect(screen.queryByText('Artist B')).not.toBeInTheDocument();
      }); 
});

describe('CompactAlbumCard', () => {
    const mockCompactAlbumFullDate = {
      id: 'album456',
      name: 'Test Album Full Date',
      images: [{ url: 'http://example.com/album-image.jpg' }],
      release_date: '2023-05-10',
      release_date_precision: 'day'
    };
  
    const mockCompactAlbumYearOnly = {
      id: 'album789',
      name: 'Test Album Year Only',
      images: [{ url: 'http://example.com/album-year-image.jpg' }],
      release_date: '2022',
      release_date_precision: 'year'
    };
  
    test('renders AlbumCard with full date precision', () => {
      render(
        <MemoryRouter>
          <CompactAlbumCard album={mockCompactAlbumFullDate} />
        </MemoryRouter>
      );
  
      expect(screen.getByText('Test Album Full Date')).toBeInTheDocument();
      expect(screen.getByText('2023')).toBeInTheDocument();
      expect(screen.getByAltText('Test Album Full Date')).toHaveAttribute('src', 'http://example.com/album-image.jpg');
      expect(screen.getByRole('link')).toHaveAttribute('href', '/album/album456');
    });
  
    test('renders AlbumCard with year only precision', () => {
      render(
        <MemoryRouter>
          <CompactAlbumCard album={mockCompactAlbumYearOnly} />
        </MemoryRouter>
      );
  
      expect(screen.getByText('Test Album Year Only')).toBeInTheDocument();
      expect(screen.getByText('2022')).toBeInTheDocument();
      expect(screen.getByAltText('Test Album Year Only')).toHaveAttribute('src', 'http://example.com/album-year-image.jpg');
      expect(screen.getByRole('link')).toHaveAttribute('href', '/album/album789');
    });
  
    test('handles missing album images gracefully', () => {
      const albumNoImage = { ...mockCompactAlbumFullDate, images: [] };
      render(
        <MemoryRouter>
          <CompactAlbumCard album={albumNoImage} />
        </MemoryRouter>
      );
      const image = screen.getByAltText('Test Album Full Date');
      expect(image).toBeInTheDocument();
      expect(image).not.toHaveAttribute('src');
    });
  });
  