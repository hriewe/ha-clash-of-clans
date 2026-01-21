# Clash of Clans – Home Assistant Integration

Custom Home Assistant integration for exposing Clash of Clans data as sensors.

## Features
- Player trophies, town hall, league
- Clan war state and timing
- HACS compatible
- UI configuration (no YAML)

## Installation (HACS)
1. HACS → Integrations
2. Custom repositories
3. Add `https://github.com/hriewe/ha-clash-of-clans`
4. Category: Integration
5. Install "Clash of Clans"
6. Restart Home Assistant

## Configuration
- API Token (from developer.clashofclans.com)
- Player Tag
- Clan Tag

## Notes
- Your Home Assistant IP must be whitelisted in the Clash of Clans developer portal
- Data updates every 5 minutes
