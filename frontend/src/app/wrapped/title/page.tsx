"use client";

import { useEffect, useRef } from "react";

const SpotifyUserPage = () => {
    const containerRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const container = containerRef.current;
        if (!container) {
            console.error("Container not found: spotifyUserContainer");
            return;
        }

        function createSection(title: string, id: string): void {
            const section = document.createElement("div");
            const heading = document.createElement("h3");
            heading.innerText = title;
            section.appendChild(heading);

            const list = document.createElement("ul");
            list.id = id;
            section.appendChild(list);

            container!.appendChild(section); // Non-null assertion here
        }

        // Build HTML structure
        const displayName = document.createElement("p");
        displayName.id = "display_name";
        container!.appendChild(displayName);

        const email = document.createElement("p");
        email.id = "email";
        container!.appendChild(email);

        const profileImage = document.createElement("img");
        profileImage.id = "profile_image";
        profileImage.alt = "Profile Image";
        profileImage.width = 100;
        profileImage.height = 100;
        container!.appendChild(profileImage);

        // Append sections for each category
        createSection("Favorite Tracks (4 weeks)", "favorite_tracks_short");
        createSection("Favorite Tracks (6 months)", "favorite_tracks_medium");
        createSection("Favorite Tracks (1 year)", "favorite_tracks_long");

        createSection("Favorite Artists (4 weeks)", "favorite_artists_short");
        createSection("Favorite Artists (6 months)", "favorite_artists_medium");
        createSection("Favorite Artists (1 year)", "favorite_artists_long");

        createSection("Favorite Genres (4 weeks)", "favorite_genres_short");
        createSection("Favorite Genres (6 months)", "favorite_genres_medium");
        createSection("Favorite Genres (1 year)", "favorite_genres_long");

        createSection("Quirkiest Artists (4 weeks)", "quirkiest_artists_short");
        createSection("Quirkiest Artists (6 months)", "quirkiest_artists_medium");
        createSection("Quirkiest Artists (1 year)", "quirkiest_artists_long");

        const llamaDescriptionSection = document.createElement("div");
        llamaDescriptionSection.innerHTML = `<h3>Llama Description</h3><p id="llama_description"></p>`;
        container!.appendChild(llamaDescriptionSection);

        const llamaSongRecsSection = document.createElement("div");
        llamaSongRecsSection.innerHTML = `<h3>Llama Song Recommendations</h3><p id="llama_songrecs"></p>`;
        container!.appendChild(llamaSongRecsSection);

        createSection("Past Roasts", "past_roasts");

        async function fetchAndDisplaySpotifyUser(): Promise<void> {
            try {
                const response = await fetch(`http://localhost:8000/spotify_data/updateuser`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include'
                });

                if (!response.ok) {
                    console.error("Failed to fetch SpotifyUser data");
                    return;
                }
                let data = await response.json();
                data = data.spotify_user;
                (document.getElementById("display_name") as HTMLElement).innerText = `Display Name: ${data.display_name}`;
                (document.getElementById("email") as HTMLElement).innerText = `Email: ${data.email}`;
                (document.getElementById("profile_image") as HTMLImageElement).src = data.profile_image_url;

                displayList("favorite_tracks_short", data.favorite_tracks_short);
                displayList("favorite_tracks_medium", data.favorite_tracks_medium);
                displayList("favorite_tracks_long", data.favorite_tracks_long);

                displayList("favorite_artists_short", data.favorite_artists_short);
                displayList("favorite_artists_medium", data.favorite_artists_medium);
                displayList("favorite_artists_long", data.favorite_artists_long);

                displayStringList("favorite_genres_short", data.favorite_genres_short);
                displayStringList("favorite_genres_medium", data.favorite_genres_medium);
                displayStringList("favorite_genres_long", data.favorite_genres_long);

                displayList("quirkiest_artists_short", data.quirkiest_artists_short);
                displayList("quirkiest_artists_medium", data.quirkiest_artists_medium);
                displayList("quirkiest_artists_long", data.quirkiest_artists_long);

                (document.getElementById("llama_description") as HTMLElement).innerText = data.llama_description;
                (document.getElementById("llama_songrecs") as HTMLElement).innerText = data.llama_songrecs;

                displayList("past_roasts", data.past_roasts);

            } catch (error) {
                console.error("Error fetching SpotifyUser data:", error);
            }
        }

        function displayList(elementId: string, items: string[]): void {
            const container = document.getElementById(elementId) as HTMLElement | null;
            if (!container) return;

            container.innerHTML = "";

            if (items && items.length > 0) {
                items.forEach((item: any) => {
                    const listItem = document.createElement("li");
                    listItem.innerText = item.name;
                    container.appendChild(listItem);
                });
            } else {
                container.innerText = "No data available";
            }
        }



           function displayStringList(elementId: string, items: string[]): void {
            const container = document.getElementById(elementId) as HTMLElement | null;
            if (!container) return;

            container.innerHTML = "";

            if (items && items.length > 0) {
                items.forEach((item: string) => {
                    const listItem = document.createElement("li");
                    listItem.innerText = item;
                    container.appendChild(listItem);
                });
            } else {
                container.innerText = "No data available";
            }
        }

        fetchAndDisplaySpotifyUser().catch(console.error);
    }, []); // Empty dependency array means this only runs once on mount

    return (
        <div id="spotifyUserContainer" ref={containerRef}>
            {/* This is where the content will be appended */}
        </div>
    );
};

export default SpotifyUserPage;
