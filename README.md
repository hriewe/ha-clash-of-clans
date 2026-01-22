# Clash of Clans – Home Assistant Integration

[![GitHub release](https://img.shields.io/github/release/hriewe/ha-clash-of-clans.svg)](https://github.com/hriewe/ha-clash-of-clans/releases)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.4.4%2B-blue.svg)](https://github.com/home-assistant/core)

Custom Home Assistant integration for exposing Clash of Clans data as sensors.

<p align="center">
  <img src="assets/sensors.png" />
</p>

## Features
- Easy to manage entities (One device per player tag)
- Player trophies, town hall, league, and many other stats
- Clan war state and timing
- HACS compatible
- UI configuration (no YAML)
- [Companion Lovelace card](https://github.com/hriewe/lovelace-clash-of-clans)

## Installation (HACS)
1. HACS → Integrations
2. Custom repositories
3. Add `https://github.com/hriewe/ha-clash-of-clans`
4. Category: Integration
5. Install "Clash of Clans"
6. Restart Home Assistant

## Configuration
- You will need an API Token from [developer.clashofclans.com](https://developer.clashofclans.com)
- Player Tag (e.g. `#2V2V2V2V`)

## Notes
- Your Home Assistant IP must be whitelisted in the Clash of Clans developer portal
- Data updates every 5 minutes
