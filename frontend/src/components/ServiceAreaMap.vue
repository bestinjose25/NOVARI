<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount,
  watch,
  nextTick
} from 'vue'

import { useI18n } from 'vue-i18n'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  height: {
    type: String,
    default: '420px',
  },
})

const { t, locale } = useI18n({
  useScope: 'global',
})


const mapContainer = ref(null)

let map = null
let markers = []


const locations = [
  {
    key: 'koblenz',
    lat: 50.3569,
    lng: 7.5890,
  },
  {
    key: 'andernach',
    lat: 50.4397,
    lng: 7.4014,
  },
  {
    key: 'neuwied',
    lat: 50.4286,
    lng: 7.4612,
  },
  {
    key: 'mayen',
    lat: 50.3284,
    lng: 7.2221,
  },
  {
    key: 'bendorf',
    lat: 50.4229,
    lng: 7.5792,
  },
  {
    key: 'weissenthurm',
    lat: 50.4175,
    lng: 7.4503,
  },
  {
    key: 'muelheimKaerlich',
    lat: 50.3856,
    lng: 7.4986,
  },
]


// ========================================
// CREATE CITY MARKERS
// ========================================

const createMarkers = () => {

  // Remove old markers
  markers.forEach((marker) => {
    marker.remove()
  })

  markers = []


  locations.forEach((location) => {

    const isKoblenz = location.key === 'koblenz'


    // Custom red location-pin icon
    const redPinIcon = L.divIcon({

      className: 'custom-map-marker',

      html: `
        <div
          class="map-pin ${isKoblenz ? 'map-pin-main' : ''}"
        >
          <div class="map-pin-dot"></div>
        </div>
      `,

      iconSize: isKoblenz
        ? [34, 44]
        : [30, 40],

      iconAnchor: isKoblenz
        ? [17, 44]
        : [15, 40],

      popupAnchor: [0, -42],

    })


    const marker = L.marker(
      [
        location.lat,
        location.lng
      ],
      {
        icon: redPinIcon,
      }
    )


    marker
      .addTo(map)

      .bindPopup(`
        <div style="
          font-size: 15px;
          font-weight: 700;
          min-width: 100px;
          text-align: center;
        ">
          ${t(`area.cities.${location.key}`)}
        </div>
      `)

      .bindTooltip(
        t(`area.cities.${location.key}`),
        {
          direction: 'top',
          offset: [0, -35],
        }
      )


    markers.push(marker)

  })
}


// ========================================
// INITIALIZE MAP
// ========================================

onMounted(async () => {

  await nextTick()


  if (!mapContainer.value) {
    return
  }


  map = L.map(
    mapContainer.value,
    {

      // Mouse / trackpad
      scrollWheelZoom: true,

      // Double click
      doubleClickZoom: true,

      // Touch screen
      touchZoom: true,

      // Allow dragging
      dragging: true,

      // Show + and - controls
      zoomControl: true,

      // Keyboard controls
      keyboard: true,

    }
  )


  // ========================================
  // OPENSTREETMAP
  // ========================================

  L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      maxZoom: 19,

      attribution:
        '&copy; OpenStreetMap contributors',
    }
  ).addTo(map)


  // Create markers
  createMarkers()


  // ========================================
  // FIT MAP TO ALL LOCATIONS
  // ========================================

  const bounds = L.latLngBounds(
    locations.map((location) => [
      location.lat,
      location.lng
    ])
  )


  map.fitBounds(
    bounds,
    {
      padding: [40, 40],
    }
  )


  // Fix size after Vue/Tailwind layout
  setTimeout(() => {

    if (map) {
      map.invalidateSize()
    }

  }, 200)

})


// ========================================
// UPDATE MARKER TEXT WHEN LANGUAGE CHANGES
// ========================================

watch(locale, () => {

  if (map) {
    createMarkers()
  }

})


// ========================================
// CLEANUP
// ========================================

onBeforeUnmount(() => {

  markers.forEach((marker) => {
    marker.remove()
  })

  markers = []


  if (map) {

    map.remove()

    map = null

  }

})
</script>


<template>
  <div
    ref="mapContainer"
    class="z-0 w-full rounded-2xl"
    :style="{ height: props.height }"
  ></div>
</template>

<style>
.custom-map-marker {
  background: transparent;
  border: none;
}


/* Main red pointing marker */
.map-pin {
  position: relative;

  width: 30px;
  height: 30px;

  background: #dc2626;

  border: 3px solid white;

  border-radius:
    50%
    50%
    50%
    0;

  transform: rotate(-45deg);

  box-shadow:
    0 3px 8px
    rgba(0, 0, 0, 0.25);
}


/* White dot inside marker */
.map-pin-dot {
  position: absolute;

  width: 8px;
  height: 8px;

  top: 50%;
  left: 50%;

  background: white;

  border-radius: 50%;

  transform:
    translate(-50%, -50%);
}


/* Koblenz slightly larger */
.map-pin-main {
  width: 34px;
  height: 34px;

  background: #b91c1c;
}
</style>