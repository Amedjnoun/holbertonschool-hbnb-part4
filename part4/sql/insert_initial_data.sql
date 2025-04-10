-- Insert initial data

-- Clear the database: delete all data from tables in order to respect foreign key constraints
DELETE FROM reviews;
DELETE FROM place_amenity;
DELETE FROM places;
DELETE FROM amenities;
DELETE FROM users;

-- Insert administrator user
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Tony',
    'Stark',
    'admin@Hairbedsnbear.com',
    '$2b$12$FKHyF05SBD9P.loYwka92ODRrbLvMcJhUnumfM7WOL.aM3tj89NCG', -- bcrypt hash of 'admin123'
    1
);

-- Insert demo users with pop culture references
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
    'Walter',
    'White',
    'heisenberg@example.com',
    '$2b$12$L/OjQw6GnrHTb42CTC.hselZc686OW.FC.PdUhmyQJTIML4nIQSD.', -- bcrypt hash of 'azerty123'
    0
),
(
    'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
    'Daenerys',
    'Targaryen',
    'motherofdragon@example.com',
    '$2b$12$pUPjGpjRIiYGfAia4Zltw.I9JdpJRSrT7mtxq879khj2oxco/FgkC', -- bcrypt hash of 'azerty123'
    0
);

-- Insert demo places for Walter White
-- Walter's Place 1: Breaking Bad reference
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    (
        '884b6b34-5c63-47e8-ab60-a7ba6a63ddd1',
        'The RV Hideaway',
        'A secluded getaway in the New Mexico desert. Perfect for chemistry enthusiasts. Not suspicious at all.',
        150.00,
        40.7128,
        -74.0060,
        'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
        '2023-01-15 09:23:45',
        '2023-04-22 14:35:12'
    );

-- Walter's Place 2: Breaking Bad reference
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    (
        'cc09352c-31a5-43ec-8786-e17a36c2ac99',
        'Los Pollos Hermanos Loft',
        'Modern apartment above a famous chicken restaurant. Very clean and organized.',
        100.00,
        51.5074,
        -0.1278,
        'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
        '2023-02-18 11:42:38',
        '2023-05-07 16:19:27'
    );

-- Walter's Place 3: Breaking Bad reference
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    (
        'a6061aab-736c-4194-8117-d4527e18795f',
        'Chemistry Teacher''s Basement',
        'Functional basement with excellent ventilation and unique equipment. Great for science projects.',
        10,
        51.5074,
        -0.1278,
        'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
        '2023-03-05 08:15:22',
        '2023-06-12 10:45:59'
    );

-- Insert demo places for Daenerys
-- Daenerys Place 1: Game of Thrones reference
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    (
        'd1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6',
        'Dragonstone Castle',
        'Ancient fortress with stunning ocean views. Dragon-friendly accommodation.',
        200.00,
        34.0522,
        -118.2437,
        'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
        '2023-01-30 13:27:19',
        '2023-05-18 09:38:42'
    );

-- Daenerys Place 2: Game of Thrones reference
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    (
        'e2f3g4h5-i6j7-k8l9-m0n1-o2p3q4r5s6t7',
        'Dothraki Tent',
        'Authentic nomadic experience in the great grass sea. Horse-friendly.',
        100.00,
        44.4280,
        -110.5885,
        'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
        '2023-02-14 15:44:33',
        '2023-06-03 12:55:17'
    );

-- Daenerys Place 3: Game of Thrones reference
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    (
        'f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8',
        'Meereen Pyramid Penthouse',
        'Luxurious top-floor accommodation with breathtaking views of the entire city.',
        300.00,
        36.7783,
        -119.4179,
        'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
        '2023-03-22 17:12:05',
        '2023-07-01 14:23:36'
    );

-- Insert reviews with pop culture references
INSERT OR IGNORE INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES
    (
        '7e2c42be-8936-4813-bba9-c623b8a98409',
        'The view from Dragonstone is amazing, but the place was a bit too drafty. I am the one who knocks... on the door because it''s so windy.',
        5,
        'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
        'd1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6',
        '2023-06-18 09:45:32',
        '2023-06-18 09:45:32'
    ),
    (
        '0e75219b-7a28-4326-a28f-357d40a1c9a4',
        'The RV was... interesting. Had to burn my clothes afterward due to a strange chemical smell. Fire and blood indeed!',
        5,
        'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
        '884b6b34-5c63-47e8-ab60-a7ba6a63ddd1',
        '2023-05-07 14:23:18',
        '2023-05-07 14:23:18'
    ),
    (
        'f45a6b1c-d2e3-4f5a-6b7c-8d9e0f1a2b3c',
        'The Dothraki tent was too small for my... needs. I need to cook... food, not sleep on the floor.',
        3,
        'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
        'e2f3g4h5-i6j7-k8l9-m0n1-o2p3q4r5s6t7',
        '2023-04-12 17:39:26',
        '2023-04-12 17:39:26'
    ),
    (
        'a1b2c3d4-e5f6-7g8h-9i0j-1a2b3c4d5e6f',
        'The Meereen Pyramid penthouse was perfect for my empire... I mean vacation plans. Very suitable for a kingpin... of relaxation.',
        5,
        'e4cb3ac8-3f11-4f9a-982e-1f6d17694c9f',
        'f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8',
        '2023-07-03 11:27:54',
        '2023-07-03 11:27:54'
    ),
    (
        '2c3d4e5f-6g7h-8i9j-0k1l-2m3n4o5p6q7r',
        'Los Pollos Hermanos Loft had great chicken nearby, but I sensed something suspicious about the owner. Fire cannot kill a dragon... or my appetite!',
        4,
        'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
        'cc09352c-31a5-43ec-8786-e17a36c2ac99',
        '2023-06-29 08:16:42',
        '2023-06-29 08:16:42'
    ),
    (
        '3d4e5f6g-7h8i-9j0k-1l2m-3n4o5p6q7r8s',
        'The basement was too dark and full of terrors... I mean strange equipment. My dragons got nervous.',
        2,
        'a0d6479b-2b2e-4948-8b35-4e9ac5c3846a',
        'a6061aab-736c-4194-8117-d4527e18795f',
        '2023-05-22 19:38:15',
        '2023-05-22 19:38:15'
    );

-- Insert amenities with pop culture twists
INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at)
VALUES
    ('a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', 'Westeros WiFi', '2023-01-05 10:15:27', '2023-01-05 10:15:27'),
    ('b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7', 'Dragon Parking', '2023-01-05 10:16:33', '2023-01-05 10:16:33'),
    ('c3d4e5f6-g7h8-i9j0-k1l2-m3n4o5p6q7r8', 'Blue Crystal Air Conditioning', '2023-01-05 10:17:45', '2023-01-05 10:17:45'),
    ('d4e5f6g7-h8i9-j0k1-l2m3-n4o5p6q7r8s9', 'Heisenberg''s Kitchen', '2023-01-05 10:18:52', '2023-01-05 10:18:52'),
    ('e5f6g7h8-i9j0-k1l2-m3n4-o5p6q7r8s9t0', 'Iron Throne TV Lounge', '2023-01-05 10:20:11', '2023-01-05 10:20:11'),
    ('f6g7h8i9-j0k1-l2m3-n4o5-p6q7r8s9t0u1', 'Valyrian Steel Washer/Dryer', '2023-01-05 10:21:23', '2023-01-05 10:21:23'),
    ('g7h8i9j0-k1l2-m3n4-o5p6-q7r8s9t0u1v2', 'Hodor Door Service', '2023-01-05 10:22:37', '2023-01-05 10:22:37');

-- Connect places with amenities
INSERT OR IGNORE INTO place_amenity (place_id, amenity_id, created_at, updated_at)
VALUES
    -- Walter's RV Hideaway
    ('884b6b34-5c63-47e8-ab60-a7ba6a63ddd1', 'a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', '2023-01-15 09:30:15', '2023-01-15 09:30:15'), -- Westeros WiFi
    ('884b6b34-5c63-47e8-ab60-a7ba6a63ddd1', 'b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7', '2023-01-15 09:30:45', '2023-01-15 09:30:45'), -- Dragon Parking
    ('884b6b34-5c63-47e8-ab60-a7ba6a63ddd1', 'c3d4e5f6-g7h8-i9j0-k1l2-m3n4o5p6q7r8', '2023-01-15 09:31:22', '2023-01-15 09:31:22'), -- Blue Crystal Air Conditioning
    ('884b6b34-5c63-47e8-ab60-a7ba6a63ddd1', 'd4e5f6g7-h8i9-j0k1-l2m3-n4o5p6q7r8s9', '2023-01-15 09:32:03', '2023-01-15 09:32:03'), -- Heisenberg's Kitchen

    -- Walter's Los Pollos Hermanos Loft
    ('cc09352c-31a5-43ec-8786-e17a36c2ac99', 'a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', '2023-02-18 12:05:32', '2023-02-18 12:05:32'), -- Westeros WiFi
    ('cc09352c-31a5-43ec-8786-e17a36c2ac99', 'c3d4e5f6-g7h8-i9j0-k1l2-m3n4o5p6q7r8', '2023-02-18 12:06:17', '2023-02-18 12:06:17'), -- Blue Crystal Air Conditioning
    ('cc09352c-31a5-43ec-8786-e17a36c2ac99', 'd4e5f6g7-h8i9-j0k1-l2m3-n4o5p6q7r8s9', '2023-02-18 12:07:03', '2023-02-18 12:07:03'), -- Heisenberg's Kitchen
    ('cc09352c-31a5-43ec-8786-e17a36c2ac99', 'e5f6g7h8-i9j0-k1l2-m3n4-o5p6q7r8s9t0', '2023-02-18 12:07:45', '2023-02-18 12:07:45'), -- Iron Throne TV Lounge

    -- Walter's Chemistry Teacher's Basement
    ('a6061aab-736c-4194-8117-d4527e18795f', 'a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', '2023-03-05 08:45:19', '2023-03-05 08:45:19'), -- Westeros WiFi
    ('a6061aab-736c-4194-8117-d4527e18795f', 'e5f6g7h8-i9j0-k1l2-m3n4-o5p6q7r8s9t0', '2023-03-05 08:46:32', '2023-03-05 08:46:32'), -- Iron Throne TV Lounge

    -- Daenerys's Dragonstone Castle
    ('d1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6', 'a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', '2023-01-30 14:12:37', '2023-01-30 14:12:37'), -- Westeros WiFi
    ('d1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6', 'c3d4e5f6-g7h8-i9j0-k1l2-m3n4o5p6q7r8', '2023-01-30 14:13:22', '2023-01-30 14:13:22'), -- Blue Crystal Air Conditioning
    ('d1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6', 'd4e5f6g7-h8i9-j0k1-l2m3-n4o5p6q7r8s9', '2023-01-30 14:14:11', '2023-01-30 14:14:11'), -- Heisenberg's Kitchen
    ('d1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6', 'f6g7h8i9-j0k1-l2m3-n4o5-p6q7r8s9t0u1', '2023-01-30 14:15:29', '2023-01-30 14:15:29'), -- Valyrian Steel Washer/Dryer
    ('d1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6', 'g7h8i9j0-k1l2-m3n4-o5p6-q7r8s9t0u1v2', '2023-01-30 14:16:18', '2023-01-30 14:16:18'), -- Hodor Door Service

    -- Daenerys's Dothraki Tent
    ('e2f3g4h5-i6j7-k8l9-m0n1-o2p3q4r5s6t7', 'd4e5f6g7-h8i9-j0k1-l2m3-n4o5p6q7r8s9', '2023-02-14 16:05:42', '2023-02-14 16:05:42'), -- Heisenberg's Kitchen
    ('e2f3g4h5-i6j7-k8l9-m0n1-o2p3q4r5s6t7', 'g7h8i9j0-k1l2-m3n4-o5p6-q7r8s9t0u1v2', '2023-02-14 16:06:33', '2023-02-14 16:06:33'), -- Hodor Door Service

    -- Daenerys's Meereen Pyramid Penthouse
    ('f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8', 'a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', '2023-03-22 17:45:12', '2023-03-22 17:45:12'), -- Westeros WiFi
    ('f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8', 'b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7', '2023-03-22 17:46:23', '2023-03-22 17:46:23'), -- Dragon Parking
    ('f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8', 'c3d4e5f6-g7h8-i9j0-k1l2-m3n4o5p6q7r8', '2023-03-22 17:47:14', '2023-03-22 17:47:14'), -- Blue Crystal Air Conditioning
    ('f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8', 'd4e5f6g7-h8i9-j0k1-l2m3-n4o5p6q7r8s9', '2023-03-22 17:48:05', '2023-03-22 17:48:05'), -- Heisenberg's Kitchen
    ('f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8', 'e5f6g7h8-i9j0-k1l2-m3n4-o5p6q7r8s9t0', '2023-03-22 17:49:22', '2023-03-22 17:49:22'), -- Iron Throne TV Lounge
    ('f3g4h5i6-j7k8-l9m0-n1o2-p3q4r5s6t7u8', 'g7h8i9j0-k1l2-m3n4-o5p6-q7r8s9t0u1v2', '2023-03-22 17:50:18', '2023-03-22 17:50:18'); -- Hodor Door Service
