# ABT UB TOO — Fare & Stop Reference
**Last updated:** 2026-06-23  
**Sources:** ABT Testing Crib Sheet CSVs (Daily Cap, Reference Fares, iLink Zone 1–NW, Bangor TS, Zone to Route Map, Zones)

---

## 1. Reference Fare Bands — Single Fares & Daily Caps

> **How single fares map to ref codes:** single fare and daily cap are both derived from the ref value in Reference Fares CSV. The cap is NOT simply 2× the single fare.

| Ref | Single Fare | Daily Cap |
|-----|-------------|-----------|
| 0.04 | — | £2.00 |
| 0.05 | — | £3.80 |
| 0.06 | — | £3.80 |
| 0.1 | £1.90 | £3.80 |
| 0.12 | — | £4.60 |
| 0.15 | — | £4.60 |
| 0.2 | £2.30 | £4.60 |
| 0.21 | — | £4.60 |
| 0.25 | £2.90 | £4.60 |
| 0.26 | — | £4.60 |
| 0.3 | — | £5.00 |
| 0.31 | — | £4.60 |
| 0.35 | £3.10 | £5.00 |
| 0.4 | — | £5.60 |
| 0.45 | £3.50 | £5.60 |
| 0.5 | — | £6.40 |
| 0.55 | £4.00 | £6.40 |
| 0.6 | £4.50 | £7.20 |
| 0.61 | — | £8.20 |
| 0.65 | — | £8.20 |
| 0.7 | £5.10 | £8.20 |
| 0.75 | £5.90 | £9.40 |
| 0.77 | — | £9.40 |
| 0.81 | — | £11.00 |
| 0.85 | £6.90 | £11.00 |
| 0.87 | — | £23.00 |
| 0.89 | — | £12.50 |
| 0.9 | — | £12.50 |
| 0.91 | — | £15.00 |
| 0.93 | — | £17.50 |
| 0.94 | — | £20.00 |
| 0.95 | — | £12.50 |
| 0.96 | — | £20.00 |
| 0.97 | — | £23.00 |
| 1.0 | — | £15.00 |
| 1.01 | — | £13.50 |
| 1.02 | — | £11.00 |
| 1.04 | — | £17.50 |
| 1.05 | £9.40 | £15.00 |
| 1.08 | — | £20.00 |
| 1.1 | — | £17.50 |
| 1.15 | £11.00 | £17.50 |
| 1.2 | — | £20.00 |
| 1.25 | — | £20.00 |
| 1.3–1.6 | — | £23.00 |
| 1.61 | — | £17.10 |
| 6.51 | — | £6.40 |

> **Mixed ref rule:** if two or more taps on the same day have **different** ref values, no single-ref daily cap applies — only a zone cap can govern. This is the key mechanism behind ref cap tests.

---

## 2. Zone Reference

### iLink Zone Caps (Transport Mode = All)

| Zone | Cap | Zone Number | Zone ID | Zone Area ID |
|------|-----|-------------|---------|--------------|
| iLink Zone 1 | £6.00 | 128 | 6 | 173 |
| iLink Zone 2 | £11.00 | 64 | 10 | 144 |
| iLink Zone 3 | £15.00 | 40 | 11 | 70 |
| iLink Zone 4 | £19.00 | 32 | 1,020 | 71 |
| iLink NW Zone | £15.00 | 36 | 1,013 | 72 |

### Metro Caps (Transport Mode = Bus)

| Zone | Cap | Zone Number | Zone ID |
|------|-----|-------------|---------|
| Metro Network Zone | £4.00 | 768 | 1,029 |
| Metro Transfer Zone (Zone 512) | N/A — transfer points only | 512 | 1,028 |

### Town Service Caps (Transport Mode = Bus only)

| Town | Cap | Zone Number | Zone ID |
|------|-----|-------------|---------|
| Bangor | £2.50 | 4,352 | 1,043 |
| Dungannon | — | 6,144 | 1,050 |
| Magherafelt | — | 8,192 | 1,058 |
| Newtownards | — | 9,216 | 1,062 |
| Strabane | — | 9,984 | 1,065 |
| Londonderry | — | 7,680 | 1,056 |
| Armagh | — | 2,816 | 1,037 |
| Antrim | — | 2,560 | 1,036 |
| Ballymena | — | 3,328 | 1,039 |
| Lisburn | — | 7,424 | 1,055 |
| Newry | — | 8,704 | 1,060 |
| Omagh | — | 9,472 | 1,063 |
| Portadown | — | 9,728 | 1,064 |
| Ulsterbus Town Service Zone (generic) | — | 16 | 12 |

### Other Zones

| Zone | Zone Number | Zone ID |
|------|-------------|---------|
| Northern Ireland Zone | 1,280 | 1,031 |
| Free Transfer Lanyon Place | 1,536 | 1,032 |
| Free Transfer Londonderry | 1,792 | 1,033 |
| Free Transfer Newry | 2,048 | 1,034 |
| Free Transfer Yorkgate | 2,304 | 1,035 |
| Coleraine Triangle Zone | 1,024 | 1,030 |

---

## 3. Capping Rule Priority

Caps are evaluated in this order. The first cap that applies wins.

1. **Metro cap (£4.00)** — fires when all taps are on Metro Network Zone stops. Overrides iLink Zone 1 cap.
2. **iLink Zone cap** — fires when taps are within the same iLink zone (or mixed-ref taps all within a zone).
3. **Town Service cap (e.g. £2.50 Bangor)** — fires when taps are within the named town service zone, Bus mode only.
4. **Reference fare daily cap** — fires when all taps on a day share the same ref value.
5. **No cap** — taps with mixed ref values and no shared zone → each tap charged at single fare.

> ⚠ **Zone 512 (Metro Transfer Zone):** stops like Knock Road and Beersbridge Road on 10b (IN) are transfer-only stops. They do NOT function as standard fare-collection alighting stops and will not register a fare correctly. Do not use them as alighting stops in tests.

> ⚠ **Stop-level zone membership is determined at the stop, not the route.** A stop can belong to multiple zones simultaneously (e.g. a stop on 403 (IN) may carry Magherafelt Town Service zone codes as well as Zone 4 codes), which can cause capping rule conflicts.

---

## 4. Route 72b (IN) — Dungannon → Armagh

**Operator:** Ulsterbus  
**Zones:** iLink Zone 3, iLink Zone 4 (some stops)  
**Note:** Moygashel Busby Shop and Armagh Bus Centre are iLink Zone 4 stops. If Zone 4 capping is active on the test account it will override ref cap tests.

> **Stop order (relevant stops):**  
> Dungannon Bus Station → Dungannon Market Square → Brooke Street → Howard School → Moygashel Busby Shop → Greys Farm → Grange Brigde → Todds House → Renolds Cottages → Currans Brae → Charlemont (Inward) → Traynors Metals → McCready's Corner → Mcilvanneys House → Mullylargan → Blackwatertown → Allistragh Post Office → Allens Corner(Dark Lane) → St Malachys Terrace → Armagh Bus Centre

### Portal Display Names

| Crib Sheet Name | Portal Name |
|----------------|-------------|
| Dungannon Bus Station | Dungannon Bus Station |
| Dungannon Market Square | Dungannon Market Sq |
| Brooke Street | Brooke Street/Wellington Rd |
| Howard School | Howard School Moygashel |
| Moygashel Busby Shop | Moygashel Busby Shop |
| Greys Farm | Greys Farm |
| Grange Brigde | Grange Brigde |
| Todds House | Todd'S Gate |
| Renolds Cottages | Reynolds Cottages |
| Currans Brae | Moy Currans Brae |
| Charlemont (Inward) | Charlemont (Clancys Pub) |
| Traynors Metals | Traynors Metals |
| McCready's Corner | Mccreadys Cnr |
| Mcilvanneys House | Mcilvanneys House |
| Mullylargan | Mullylargan |
| Blackwatertown | Blackwatertown |
| Allistragh Post Office | Allistragh Post Office |
| Allens Corner(Dark Lane) | Allens Cnr [Dark Lane] |
| St Malachys Terrace | St Malachys Terrace |
| Armagh Bus Centre | Armagh Buscentre |

### Complete Fare Table (72b IN, by ref)

**ref 0.1 (£1.90, cap £3.80)**

| Board | Alight |
|-------|--------|
| Allens Corner(Dark Lane) | Armagh Bus Centre |
| Allens Corner(Dark Lane) | St Malachys Terrace |
| Allistragh Post Office | Allens Corner(Dark Lane) |
| Blackwatertown | Mcilvanneys House |
| Blackwatertown | Mullylargan |
| Currans Brae | Charlemont (Inward) |
| Grange Brigde | Renolds Cottages |
| Grange Brigde | Todds House |
| Greys Farm | Grange Brigde |
| Greys Farm | Todds House |
| Howard School | Greys Farm |
| McCready's Corner | Allens Corner(Dark Lane) |
| McCready's Corner | Allistragh Post Office |
| Mcilvanneys House | Allistragh Post Office |
| Mcilvanneys House | McCready's Corner |
| Moygashel Busby Shop | Greys Farm |
| Mullylargan | Allistragh Post Office |
| Mullylargan | McCready's Corner |
| Mullylargan | Mcilvanneys House |
| Renolds Cottages | Charlemont (Inward) |
| Renolds Cottages | Currans Brae |
| St Malachys Terrace | Armagh Bus Centre |
| Todds House | Renolds Cottages |
| Traynors Metals | Blackwatertown |
| Traynors Metals | Mcilvanneys House |
| Traynors Metals | Mullylargan |

**ref 0.2 (£2.30, cap £4.60)**

| Board | Alight |
|-------|--------|
| Allistragh Post Office | Armagh Bus Centre |
| Allistragh Post Office | St Malachys Terrace |
| Blackwatertown | Allistragh Post Office |
| Blackwatertown | McCready's Corner |
| Brooke Street | Grange Brigde |
| Brooke Street | Greys Farm |
| Brooke Street | Todds House |
| Charlemont (Inward) | Traynors Metals |
| Currans Brae | Traynors Metals |
| Dungannon Bus Station | Greys Farm |
| Dungannon Market Square | Greys Farm |
| Grange Brigde | Charlemont (Inward) |
| Grange Brigde | Currans Brae |
| Greys Farm | Currans Brae |
| Greys Farm | Renolds Cottages |
| Howard School | Grange Brigde |
| Howard School | Todds House |
| McCready's Corner | St Malachys Terrace |
| Mcilvanneys House | Allens Corner(Dark Lane) |
| Moygashel Busby Shop | Grange Brigde |
| Moygashel Busby Shop | Renolds Cottages |
| Moygashel Busby Shop | Todds House |
| Mullylargan | Allens Corner(Dark Lane) |
| Todds House | Charlemont (Inward) |
| Todds House | Currans Brae |
| Traynors Metals | Allistragh Post Office |
| Traynors Metals | McCready's Corner |

**ref 0.25 (£2.90, cap £4.60)**

| Board | Alight |
|-------|--------|
| Blackwatertown | Allens Corner(Dark Lane) |
| Brooke Street | Renolds Cottages |
| Charlemont (Inward) | Mcilvanneys House |
| Charlemont (Inward) | Mullylargan |
| Currans Brae | Mcilvanneys House |
| Currans Brae | Mullylargan |
| Dungannon Bus Station | Grange Brigde |
| Dungannon Bus Station | Todds House |
| Dungannon Market Square | Grange Brigde |
| Dungannon Market Square | Todds House |
| Greys Farm | Charlemont (Inward) |
| Howard School | Renolds Cottages |
| McCready's Corner | Armagh Bus Centre |
| Mcilvanneys House | Armagh Bus Centre |
| Mcilvanneys House | St Malachys Terrace |
| Moygashel Busby Shop | Currans Brae |
| Mullylargan | St Malachys Terrace |
| Renolds Cottages | Traynors Metals |
| Traynors Metals | Allens Corner(Dark Lane) |

**ref 0.35 (£3.10, cap £5.00)**

| Board | Alight |
|-------|--------|
| Blackwatertown | St Malachys Terrace |
| Brooke Street | Currans Brae |
| Charlemont (Inward) | Allistragh Post Office |
| Charlemont (Inward) | Blackwatertown |
| Charlemont (Inward) | McCready's Corner |
| Currans Brae | Allistragh Post Office |
| Currans Brae | Blackwatertown |
| Currans Brae | McCready's Corner |
| Dungannon Bus Station | Renolds Cottages |
| Dungannon Market Square | Renolds Cottages |
| Grange Brigde | Traynors Metals |
| Greys Farm | Allens Corner(Dark Lane) |
| Howard School | Charlemont (Inward) |
| Howard School | Currans Brae |
| Moygashel Busby Shop | Charlemont (Inward) |
| Mullylargan | Armagh Bus Centre |
| Renolds Cottages | Mcilvanneys House |
| Renolds Cottages | Mullylargan |
| Todds House | Traynors Metals |
| Traynors Metals | St Malachys Terrace |

**ref 0.45 (£3.50, cap £5.60)**

| Board | Alight |
|-------|--------|
| Blackwatertown | Armagh Bus Centre |
| Brooke Street | Charlemont (Inward) |
| Brooke Street | Traynors Metals |
| Charlemont (Inward) | Allens Corner(Dark Lane) |
| Charlemont (Inward) | Armagh Bus Centre |
| Charlemont (Inward) | St Malachys Terrace |
| Currans Brae | Allens Corner(Dark Lane) |
| Currans Brae | Armagh Bus Centre |
| Currans Brae | St Malachys Terrace |
| Dungannon Bus Station | Charlemont (Inward) |
| Dungannon Bus Station | Currans Brae |
| Dungannon Market Square | Charlemont (Inward) |
| Dungannon Market Square | Currans Brae |
| Grange Brigde | Allistragh Post Office |
| Grange Brigde | Blackwatertown |
| Grange Brigde | McCready's Corner |
| Grange Brigde | Mcilvanneys House |
| Grange Brigde | Mullylargan |
| Greys Farm | Allistragh Post Office |
| Greys Farm | Blackwatertown |
| Greys Farm | McCready's Corner |
| Greys Farm | Mcilvanneys House |
| Greys Farm | Mullylargan |
| Greys Farm | Traynors Metals |
| Howard School | Traynors Metals |
| Moygashel Busby Shop | Mcilvanneys House |
| Moygashel Busby Shop | Mullylargan |
| Moygashel Busby Shop | Traynors Metals |
| Renolds Cottages | Allens Corner(Dark Lane) |
| Renolds Cottages | Allistragh Post Office |
| Renolds Cottages | Blackwatertown |
| Renolds Cottages | McCready's Corner |
| Todds House | Allistragh Post Office |
| Todds House | Blackwatertown |
| Todds House | McCready's Corner |
| Todds House | Mcilvanneys House |
| Todds House | Mullylargan |
| Traynors Metals | Armagh Bus Centre |

**ref 0.55 (£4.00, cap £6.40)**

| Board | Alight |
|-------|--------|
| Brooke Street | Allistragh Post Office |
| Brooke Street | Blackwatertown |
| Brooke Street | McCready's Corner |
| Brooke Street | Mcilvanneys House |
| Brooke Street | Mullylargan |
| Dungannon Bus Station | Allistragh Post Office |
| Dungannon Bus Station | Blackwatertown |
| Dungannon Bus Station | McCready's Corner |
| Dungannon Bus Station | Mcilvanneys House |
| Dungannon Bus Station | Mullylargan |
| Dungannon Bus Station | Traynors Metals |
| Dungannon Market Square | Allistragh Post Office |
| Dungannon Market Square | Blackwatertown |
| Dungannon Market Square | McCready's Corner |
| Dungannon Market Square | Mcilvanneys House |
| Dungannon Market Square | Mullylargan |
| Dungannon Market Square | Traynors Metals |
| Grange Brigde | Allens Corner(Dark Lane) |
| Grange Brigde | Armagh Bus Centre |
| Grange Brigde | St Malachys Terrace |
| **Greys Farm** | **Allens Corner(Dark Lane)** |
| **Greys Farm** | **St Malachys Terrace** ← ⚠ this is ref 0.55 NOT 0.6 |
| Howard School | Allistragh Post Office |
| Howard School | Blackwatertown |
| Howard School | McCready's Corner |
| Howard School | Mcilvanneys House |
| Howard School | Mullylargan |
| **Moygashel Busby Shop** | **Allens Corner(Dark Lane)** ← ref 0.55 NOT 0.6 |
| Moygashel Busby Shop | Allistragh Post Office |
| Moygashel Busby Shop | Blackwatertown |
| Moygashel Busby Shop | McCready's Corner |
| Renolds Cottages | Armagh Bus Centre |
| Renolds Cottages | St Malachys Terrace |
| Todds House | Allens Corner(Dark Lane) |
| Todds House | Armagh Bus Centre |
| Todds House | St Malachys Terrace |

**ref 0.6 (£4.50, cap £7.20)**

| Board | Alight |
|-------|--------|
| Brooke Street | Allens Corner(Dark Lane) |
| Brooke Street | St Malachys Terrace |
| Dungannon Bus Station | Allens Corner(Dark Lane) |
| Dungannon Market Square | Allens Corner(Dark Lane) |
| **Greys Farm** | **Armagh Bus Centre** |
| Howard School | Allens Corner(Dark Lane) |
| Howard School | Armagh Bus Centre |
| Howard School | St Malachys Terrace |
| **Moygashel Busby Shop** | **Armagh Bus Centre** |
| **Moygashel Busby Shop** | **St Malachys Terrace** |

**ref 0.7 (£5.10, cap £8.20)**

| Board | Alight |
|-------|--------|
| Brooke Street | Armagh Bus Centre |
| **Dungannon Bus Station** | **Armagh Bus Centre** |
| **Dungannon Bus Station** | **St Malachys Terrace** |
| Dungannon Market Square | Armagh Bus Centre |
| Dungannon Market Square | St Malachys Terrace |

---

## 5. Route 100b (IN) — Castlederg → Strabane

**Operator:** Ulsterbus  
**Zones:** iLink Zone 3, iLink Zone 4, iLink NW Zone, Strabane Town Service

### iLink Zone 4 Stops (all stops orders 0–8 are Zone 4)

| Order | Crib Sheet Name | Portal Name |
|-------|----------------|-------------|
| 0 | Castlederg | Castlederg |
| 1 | Spamount Crossroads | Spamount Crossroads |
| 2 | Fyfin Po | Fyfin Post Office |
| 3 | The Glen | Concess Road |
| 4 | Ardstraw Road | Ardstraw Rd |
| 5 | Victoria Bge | Victoria Bridge |
| 6 | Sion Mills | Millhaven Sion Mills |
| 7 | Glebe Park | Glebe Park |
| 8 | Clady Bge | Clady Bridge |

**Stops after Clady Bge (Zone NW / Strabane area):**

| Crib Sheet Name | Portal Name |
|----------------|-------------|
| Melmount Rd | Russells Bakery |
| Strabane, Abercorn Square | Strabane Square |
| Strabane Buscentre | Strabane Buscentre |

### Complete Fare Table (100b IN, by ref)

> Note: ref 3.1 entries (e.g. Melmount Rd → Strabane Buscentre) are data anomalies — do not use.

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| Castlederg | Spamount Crossroads | 0.1 | £1.90 |
| Fyfin Po | The Glen | 0.1 | £1.90 |
| Sion Mills | Glebe Park | 0.1 | £1.90 |
| The Glen | Ardstraw Road | 0.1 | £1.90 |
| The Glen | Victoria Bge | 0.1 | £1.90 |
| Ardstraw Road | Victoria Bge | 0.2 | £2.30 |
| Fyfin Po | Victoria Bge | 0.2 | £2.30 |
| Glebe Park | Clady Bge | 0.2 | £2.30 |
| Spamount Crossroads | Fyfin Po | 0.2 | £2.30 |
| Victoria Bge | Clady Bge | 0.2 | £2.30 |
| Victoria Bge | Glebe Park | 0.2 | £2.30 |
| Clady Bge | Melmount Rd | 0.25 | £2.90 |
| Sion Mills | Clady Bge | 0.25 | £2.90 |
| Sion Mills | Strabane Buscentre | 0.25 | £2.90 |
| Spamount Crossroads | The Glen | 0.25 | £2.90 |
| The Glen | Glebe Park | 0.25 | £2.90 |
| Ardstraw Road | Clady Bge | 0.35 | £3.10 |
| Castlederg | Fyfin Po | 0.35 | £3.10 |
| Clady Bge | Strabane Buscentre | 0.35 | £3.10 |
| Glebe Park | Melmount Rd | 0.35 | £3.10 |
| Glebe Park | Strabane Buscentre | 0.35 | £3.10 |
| Sion Mills | Melmount Rd | 0.35 | £3.10 |
| Spamount Crossroads | Ardstraw Road | 0.35 | £3.10 |
| The Glen | Clady Bge | 0.35 | £3.10 |
| Victoria Bge | Melmount Rd | 0.35 | £3.10 |
| Victoria Bge | Strabane Buscentre | 0.35 | £3.10 |
| Ardstraw Road | Glebe Park | 0.45 | £3.50 |
| Ardstraw Road | Melmount Rd | 0.45 | £3.50 |
| Ardstraw Road | Strabane Buscentre | 0.45 | £3.50 |
| Castlederg | Ardstraw Road | 0.45 | £3.50 |
| Castlederg | The Glen | 0.45 | £3.50 |
| Castlederg | Victoria Bge | 0.45 | £3.50 |
| Fyfin Po | Clady Bge | 0.45 | £3.50 |
| Fyfin Po | Glebe Park | 0.45 | £3.50 |
| Fyfin Po | Melmount Rd | 0.45 | £3.50 |
| Spamount Crossroads | Victoria Bge | 0.45 | £3.50 |
| The Glen | Melmount Rd | 0.45 | £3.50 |
| The Glen | Strabane Buscentre | 0.45 | £3.50 |
| Castlederg | Glebe Park | 0.55 | £4.00 |
| Castlederg | Melmount Rd | 0.55 | £4.00 |
| Fyfin Po | Strabane Buscentre | 0.55 | £4.00 |
| Spamount Crossroads | Clady Bge | 0.55 | £4.00 |
| Spamount Crossroads | Glebe Park | 0.55 | £4.00 |
| Spamount Crossroads | Melmount Rd | 0.55 | £4.00 |
| Spamount Crossroads | Strabane Buscentre | 0.55 | £4.00 |
| **Castlederg** | **Clady Bge** | **0.6** | **£4.50** |
| **Castlederg** | **Strabane Buscentre** | **0.6** | **£4.50** |
| Londonderry (Transfer) | Strabane Buscentre | 0.7 | £5.10 |
| Melmount Rd | Londonderry (Transfer) | 0.7 | £5.10 |
| Ardstraw Road | Londonderry (Transfer) | 0.85 | £6.90 |
| Clady Bge | Londonderry (Transfer) | 0.85 | £6.90 |
| Glebe Park | Londonderry (Transfer) | 0.85 | £6.90 |
| Sion Mills | Londonderry (Transfer) | 0.85 | £6.90 |
| The Glen | Londonderry (Transfer) | 0.85 | £6.90 |
| Victoria Bge | Londonderry (Transfer) | 0.85 | £6.90 |
| Fyfin Po | Londonderry (Transfer) | 0.95 | £5.90 |
| Spamount Crossroads | Londonderry (Transfer) | 0.95 | £5.90 |
| Castlederg | Londonderry (Transfer) | 1.05 | £9.40 |

---

## 6. Route 102a (IN) — Strabane → Londonderry

**Operator:** Ulsterbus  
**Zones:** iLink NW Zone, Strabane Town Service, Londonderry Town Service

### iLink Zone NW Stops (all stops orders 0–16 confirmed Zone NW)

| Order | Crib Sheet Name | Notes |
|-------|----------------|-------|
| 0 | Strabane Buscentre | |
| 1 | Strabane Canal St | |
| 2 | Strabane Tech | |
| 3 | Artigarvan | |
| 5 | Artigarvan, Liscurry Gardens | |
| 6 | Ballaghalare | |
| 7 | Donemana | |
| 8 | Tullyard Bridge | |
| 9 | Three Roads End | |
| 10 | Mountcastle Cemetery | |
| 11 | Desertone Rd | |
| 12 | Newbuildings, Woodside Road | |
| 13 | Golf Club | |
| 14 | Black Gates | |
| 15 | Victoria Road | |
| 16 | Peace Park | Last stop |

### Key Fare Pairs (102a IN)

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| Strabane Buscentre | Strabane Canal St | 0.1 | £1.90 |
| Strabane Buscentre | Strabane Tech | 0.1 | £1.90 |
| Strabane Buscentre | Artigarvan | 0.2 | £2.30 |
| Strabane Buscentre | Ballaghalare | 0.45 | £3.50 |
| Strabane Buscentre | Donemana | 0.45 | £3.50 |
| Strabane Buscentre | Mountcastle Cemetery | 0.55 | £4.00 |
| Strabane Buscentre | Desertone Rd | 0.7 | £5.10 |
| Strabane Buscentre | Black Gates | 0.75 | £5.90 |
| **Strabane Buscentre** | **Victoria Road** | **0.85** | **£6.90** |
| Strabane Buscentre | Peace Park | — | confirm in portal |

Zone NW cap: £15.00 — 3 taps at ref 0.85 = £20.70 > £15.00, cap fires.

---

## 7. Route 10b (IN) — Cloughey → Belfast

**Operator:** Ulsterbus  
**Direction:** IN = Cloughey → Belfast  
**Zones:** iLink Zone 3 (orders 0–22), iLink Zone 2 (orders 23–26), iLink Zone 1 / Metro (orders 27–32)

### Zone Breakdown

| Stop Order Range | Stops | Zone |
|-----------------|-------|------|
| 0–22 | Portaferry Square → Finlays Road | iLink Zone 3 |
| 23–26 | Teale Rocks, Bus Garage, Gibsons Lane, Layby | iLink Zone 2 |
| 27–32 | High School → City Hall | iLink Zone 1 + Metro Network Zone |

### iLink Zone 3 Stops (orders 0–22, confirmed)

| Order | Stop Name |
|-------|-----------|
| 0 | Portaferry, Square |
| 1 | Derry Corner |
| 2 | Nunsbridge |
| 3 | Cloughey, Thompsons Corner |
| 4 | Mageeans Corner |
| 5 | Ratalla Cottages |
| 6 | Portavogie School |
| 7 | Hughes Corner |
| 8 | Lemons Road |
| 9 | Ballyeasbrough Church |
| 10 | Glastry School |
| 11 | Rubane |
| 12 | Kircubbin, Roden Street |
| 13 | Nunsquarter Chapel |
| 14 | Ballygarvin |
| 15 | Kings Corner |
| 16 | Main Street |
| 17 | Model Farm |
| 18 | Mountstewart |
| 19 | Millars Corner |
| 20 | Cunningburn Road Junction |
| 21 | Ballyhaft |
| 22 | Finlays Road |

### iLink Zone 1 / Metro Stops (orders 27–32)

| Order | Stop Name | Notes |
|-------|-----------|-------|
| 27 | High School | ✓ Use for alighting |
| 28 | Cherry Hill | ✓ Use for alighting |
| 29 | Ulster Hospital | ✓ Use for alighting |
| 30 | Knock Road | ⚠ Zone 512 (Metro Transfer) — do NOT use as alighting |
| 31 | Beersbridge Road | ⚠ Zone 512 (Metro Transfer) — do NOT use as alighting |
| 32 | City Hall | ✓ Use for alighting |

### Key Fare Pairs (10b IN)

**Zone 3 pairs:**

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| Portaferry Square | Mountstewart | 0.7 | £5.10 |
| Portaferry Square | Cunningburn Road Junction | 0.7 | £5.10 |
| Portaferry Square | Finlays Road | 0.75 | £5.90 |

**Zone 1 (Metro zone) pairs:**

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| High School | Ulster Hospital | 0.1 | £1.90 |
| High School | Cherry Hill | 0.2 | £2.30 |
| High School | City Hall | 0.35 | £3.10 |

> ⚠ **TC-Z1 BLOCKED:** all Zone 1 UB stops on 10b (IN) are simultaneously Metro Network Zone stops. Metro cap (£4.00) fires before iLink Zone 1 cap (£6.00). A pure UB journey within Zone 1 on 10b (IN) will cap at Metro £4.00, not Zone 1 £6.00. Confirm with product/config team before running Zone 1 tests.

> ⚠ **TC-M2/M3 direction:** Metro zone stops are at the END of 10b (IN) (orders 27–32). Correcting to an outside-Metro stop at higher fare requires stops after City Hall (order 32+) which don't exist. 10b (OUT) may be the right direction — Metro zone is at the START on OUT direction. Confirm in portal before running.

---

## 8. Route 105a (IN) — Dundrod → Lisburn

**Operator:** Ulsterbus  
**Zones:** iLink Zone 2, Lisburn Town Service

### iLink Zone 2 Stops (all stops orders 0–10 confirmed Zone 2)

| Order | Stop Name |
|-------|-----------|
| 0 | Tullyrusk Road |
| 1 | Dundrod |
| 2 | Wyebridge |
| 3 | Stonyford X Roads |
| 4 | Tommys Cnr |
| 5 | Sales Cnr |
| 6 | Belshaws Quarry |
| 7 | Killowen Hospital |
| 8 | Beechdene Drive |
| 9 | Duncans Road |
| 10 | Park Gates | Last stop |

### Key Fare Pairs (105a IN)

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| Tullyrusk Road | Beechdene Drive | 0.6 | £4.50 |
| Dundrod | Beechdene Drive | 0.6 | £4.50 |
| Tullyrusk Road | Park Gates | 0.7 | confirm in portal |

Zone 2 cap: £11.00 — 3 taps at ref 0.6 = £13.50 > £11.00, cap fires.

> Note: bare "105 (IN)" is also Zone 2 but has entries in Reference Fares too. 105a (IN) is the confirmed working route.

---

## 9. Route 203b (IN) — Bangor Town Service

**Operator:** Ulsterbus  
**Zones:** Bangor Town Service Zone, iLink Zone 1, Metro Network Zone, Metro Transfer Zone (further along route)

**Bangor Town Service cap: £2.50 (Bus mode only)**

### Confirmed Bangor TS Zone Stops on 203b (IN)

| Order | Crib Sheet Name | Portal Display Name |
|-------|----------------|---------------------|
| 0 | Ballymacormick Road | **Groomsport Roundabout** |
| 1 | Dixon Road | **Carolhill/ Dixon Rd** |
| 2 | Gransha Roundabout | **Gransha Road Roundabout** |
| 3 | Rathgill Terminus | **Rathgill Estate** |
| 4 | Ballyree Drive | **Bloomfield Estate** |
| 5 | St.Andrews Church | **Football Grounds** |
| 6 | 100 Skipperstone Rd | **Whitehill Est (Main Ent)** |
| 7 | Ravara | **Kilcooley** |

Stops after Ravara (order 8+) — e.g. City Hall — are **outside** Bangor TS zone.

### Fare Pairs Within Bangor TS Zone (both board and alight in zone)

| Board (portal name) | Alight (portal name) | Ref | Single |
|---------------------|----------------------|-----|--------|
| Groomsport Roundabout | Carolhill/ Dixon Rd | 0.1 | £1.90 |
| Groomsport Roundabout | Gransha Road Roundabout | 0.2 | £2.30 |
| Groomsport Roundabout | Rathgill Estate | 0.2 | £2.30 |
| Groomsport Roundabout | Bloomfield Estate | 0.2 | £2.30 |
| Groomsport Roundabout | Whitehill Est (Main Ent) | 0.25 | £2.90 |
| Groomsport Roundabout | Kilcooley | 0.35 | £3.10 |
| Carolhill/ Dixon Rd | Gransha Road Roundabout | 0.1 | £1.90 |
| Carolhill/ Dixon Rd | Rathgill Estate | 0.1 | £1.90 |
| Carolhill/ Dixon Rd | Bloomfield Estate | 0.2 | £2.30 |
| Carolhill/ Dixon Rd | Whitehill Est (Main Ent) | 0.2 | £2.30 |
| Carolhill/ Dixon Rd | Kilcooley | 0.25 | £2.90 |
| Gransha Road Roundabout | Kilcooley | 0.25 | £2.90 |
| Bloomfield Estate | Kilcooley | 0.25 | £2.90 |
| Whitehill Est (Main Ent) | Kilcooley | 0.1 | £1.90 |

### Fare Pairs Outside Bangor TS Zone (higher-fare correction targets)

| Board (portal name) | Alight | Ref | Single |
|---------------------|--------|-----|--------|
| Groomsport Roundabout | City Hall | 0.7 | £5.10 |
| Carolhill/ Dixon Rd | City Hall | 0.7 | £5.10 |
| Rathgill Estate | City Hall | 0.6 | £4.50 |
| Bloomfield Estate | City Hall | 0.6 | £4.50 |

> ⚠ **Route 1 (IN) warning:** only 3 stops on route 1 (IN) are in Bangor TS zone — Stand 2 (0), Woodgreen (1), 74 Rathmore Road (2). All stops beyond order 2 (Ballymullan Road, Crawfordsburn Inn, etc.) are outside the zone. Use 203b (IN) for Bangor TS tests.

---

## 10. Route 1 (IN) — Belfast → Bangor (via Rathmore)

**Operator:** Ulsterbus  
**Zones:** iLink Zone 1, iLink Zone 2, Bangor Town Service (first 3 stops only), Metro Network Zone  
**ServiceID:** 1530

### Bangor TS Zone Stops on Route 1 (IN) — only 3

| Order | Stop Name |
|-------|-----------|
| 0 | Stand 2 |
| 1 | Woodgreen |
| 2 | 74 Rathmore Road |

### Key Fare Pairs (1 IN)

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| 74 Rathmore Road | Ballymullan Road | 0.1 | £1.90 |
| 74 Rathmore Road | Crawfordsburn Village | 0.1 | £1.90 |
| 74 Rathmore Road | Laganside Bus Std. | 0.55 | £4.00 |

---

## 11. Route 403 (IN) — Magherafelt → Omagh area

**Operator:** Ulsterbus  
**Zones:** iLink Zone 4, Magherafelt Town Service, Dungannon Town Service

> ⚠ **Zone 4 test warning:** Magherafelt Depot (boarding stop) carries Town Service zone codes (16, 8192 = Magherafelt TS) in addition to Zone 4 code (32). These extra zone codes are NOT in Zone 4 rule's AssignedZones, causing BestFareCalculator to inconsistently include/exclude the tap from the Zone 4 cap calculation. Do NOT use 403 (IN) for Zone 4 cap tests — use 100b (IN) only.

> ⚠ **FileNumber:** manually created test taps on 403 (IN) have an empty FileNumber field (no physical card reader tap), which further complicates invoice processing. 100b (IN) taps from a real card have a populated FileNumber.

### Key Fare Pairs (403 IN — reference only)

| Board | Alight | Ref | Single |
|-------|--------|-----|--------|
| Magherafelt Depot | Beattie Park | 1.15 | £11.00 |
| Magherafelt Depot | Halfway House | 1.05 | £9.40 |
| Magherafelt Depot | Desertmartin | 0.25 | £2.90 |
| Cranagh | Beattie Park | 0.85 | £6.90 |
| Draperstown | Browns Pub House | 0.55 | £4.00 |

---

## 12. Route 302d (OUT) — Bangor Town Service (alternative)

**Operator:** Ulsterbus  
**Zones:** Bangor Town Service Zone  
**ServiceID:** 1548

### Key Fare Pairs (302d OUT)

| Board | Alight | Ref | Notes |
|-------|--------|-----|-------|
| Arras Pk | Bottom Breezemount Park | 0.1 | Within UBTS |
| Stand 7 | Bottom Breezemount Park | 0.2 | Within UBTS |
| Arras Pk | Belfast (Transfer) | 0.6 | Outside UBTS |
| Rathgill Terminus | Belfast (Transfer) | 0.6 | Outside UBTS |
| Bloomfield Roundabout | Belfast (Transfer) | 0.6 | Outside UBTS |
| Balloo Drive / Rathgael House | Belfast (Transfer) | 0.7 | Outside UBTS |
| Stand 7 | Newtownards (Transfer) | 0.61 | Outside UBTS — ref.61 band, cap £8.20 |

---

## 13. Zone to Route Summary

Routes confirmed in each zone (from Zone to Route Map CSV):

| Zone | Confirmed Routes (IN direction) |
|------|--------------------------------|
| iLink Zone 1 | 10b, 103, 103c, 106, 106b, 107, 109, 109a, 1, 203b, 203a, and many Metro routes |
| iLink Zone 2 | 105a, 105, 10b, 103, 103c, 106, 109a, 10a, 1, 203b, 108a, 108c, 109c, 109d |
| iLink Zone 3 | 10b, 100a, 100b, 100c, 109a, 109d, 273, and others |
| iLink Zone 4 | 100b, 100c, 100l, 100a, 72b (some stops), 403 |
| iLink Zone NW | 102a, 102, 102c, 100a, 100b, 100c |
| Bangor TS | 1, 203a, 203b, 2a, 3, 3a, 4, 6, 6b, 302a–g, 303a, 404, 502a, 502b, 8001 |
| Dungannon TS | 72b (some stops) |
| Magherafelt TS | 403 (some stops) |

---

## 14. Service IDs (CloudFare env5)

| Route | ServiceID | ServiceMasterID | Description |
|-------|-----------|-----------------|-------------|
| 1 | 1530 | 88666 | Belfast - Bangor Via Rathmore |
| 10b | 1595 | 114163 | Cloughey-Portaferry-Belfast |
| 72b | 2110 | 179259 | Armagh - Dungannon Via B'watertown |
| 100b | 1755 | 140483 | Strabane - Clady - Glebe Park - Castlederg |
| 100c | 1756 | 140655 | Strabane - Clady - Glebe Park - Castlederg |
| 100l | 1757 | 140768 | Strabane - Clady - Glebe Park - Castlederg |
| 102a | 1760 | 141083 | Londonderry - Donemana - Strabane |
| 105 | 2242 | 194435 | Dundrod - Jordan's Corner - Wyebridge - Lisburn |
| 273 | 1783 | 144895 | Belfast - Dungannon - Omagh - L'derry |
| 302d | 1548 | 91560 | Bangor Town Service - Rathgill & Bloomfield |

**Operator IDs:** Translink = 1, Ulsterbus = 4, ETM Ulsterbus = 10069, Metro = 2

---

## 15. Known Data Anomalies

| Issue | Detail |
|-------|--------|
| ref 3.1 entries in 203b (IN) and 100b (IN) | Appear on pairs where route order logic reverses (e.g. Gransha Roundabout→Rathgill Terminus). Treat as invalid — do not use these pairs for testing. |
| Greys Farm → St Malachys Terrace | Ref is **0.55** in Reference Fares CSV. ABT.md incorrectly states 0.6. |
| Moygashel Busby Shop → Allens Corner(Dark Lane) | Ref is **0.55**, not 0.6. |
| 100a (IN) | Has no entries in Reference Fares CSV. Use 100b or 100c for Castlederg area tests. |
| 100l (IN) | Only 2 Zone 4 stops (Mulvin Rd, Glebe Park). Not suitable for Zone 4 cap tests. |
| 273 (IN) | Most Zone 3 stops are Transfer stops — not suitable for Zone 3 fare-collection tests. Use 10b (IN) instead. |
| Route 403 (IN) Zone 4 conflict | Magherafelt Depot carries Magherafelt TS zone codes (16, 8192) alongside Zone 4 (32). Causes BestFareCalculator inconsistency. |
