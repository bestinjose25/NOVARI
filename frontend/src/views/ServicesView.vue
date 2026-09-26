<script setup>
import { useI18n } from 'vue-i18n'

import movingImage from '../assets/images/services/ResidentialMove.jpeg'
import transportImage from '../assets/images/services/Furniture.jpeg'
import assemblyImage from '../assets/images/services/Assembly.jpeg'
import clearanceImage from '../assets/images/services/Clearance.jpeg'
import carryingImage from '../assets/images/services/CarryAssistance.jpeg'
import Footer from '@/components/Footer.vue';


const { t, tm } = useI18n({
  useScope: 'global',
})

const services = [
  {
    key: 'moving',
    image: movingImage,
  },
  {
    key: 'transport',
    image: transportImage,
  },
  {
    key: 'assembly',
    image: assemblyImage,
  },
  {
    key: 'clearance',
    image: clearanceImage,
  },
  {
    key: 'support',
    image: carryingImage,
  },
]
</script>


<template>
  <main class="services-page">

    <!-- ======================================
         HERO
    ======================================= -->
    <section class="services-hero">

      <div class="services-wrap">

        <span class="eyebrow">
          {{ t('servicesPage.hero.eyebrow') }}
        </span>

        <h1>
          {{ t('servicesPage.hero.title') }}
        </h1>

        <p>
          {{ t('servicesPage.hero.description') }}
        </p>

      </div>

    </section>


    <!-- ======================================
         SERVICES
    ======================================= -->
    <section class="services-section">

      <div class="services-wrap service-rows">

        <article
          v-for="service in services"
          :key="service.key"
          class="service-row"
        >

          <!-- CONTENT -->
          <div class="service-body">

            <span class="service-tag">
              {{
                t(
                  `servicesPage.items.${service.key}.category`
                )
              }}
            </span>


            <h3>
              {{
                t(
                  `servicesPage.items.${service.key}.title`
                )
              }}
            </h3>


            <p>
              {{
                t(
                  `servicesPage.items.${service.key}.description`
                )
              }}
            </p>


            <!-- EXAMPLES -->
            <div class="service-examples">

              <span
                v-for="example in tm(
                  `servicesPage.items.${service.key}.tags`
                )"
                :key="example"
              >
                {{ example }}
              </span>

            </div>


            <!-- BUTTON -->
            <RouterLink
              to="/quote"
              class="service-button"
            >
              {{ t('servicesPage.requestButton') }}
            </RouterLink>

          </div>


          <!-- IMAGE -->
          <div class="service-media">

            <img
              :src="service.image"
              :alt="
                t(
                  `servicesPage.items.${service.key}.title`
                )
              "
            >

          </div>

        </article>

      </div>

    </section>


    <!-- ======================================
         FINAL CTA
    ======================================= -->
    <section class="services-cta">

      <div class="services-wrap cta-inner">

        <h2>
          {{ t('servicesPage.cta.title') }}
        </h2>


        <div class="cta-actions">

          <RouterLink
            to="/quote"
            class="cta-button primary"
          >
            {{ t('servicesPage.cta.quote') }}
          </RouterLink>


          <RouterLink
            to="/contact"
            class="cta-button outline"
          >
            {{ t('servicesPage.cta.contact') }}
          </RouterLink>

        </div>

      </div>
      
    </section>
  <Footer />
  </main>
</template>


<style scoped>
.services-page {
  background: var(--paper);
  color: var(--ink);

  font-family: var(--body);
}


/* =========================================
   WRAPPER
========================================= */

.services-wrap {
  width: 100%;

  max-width: 1180px;

  margin-inline: auto;

  padding-inline:
    clamp(18px, 4vw, 32px);
}


/* =========================================
   HERO
========================================= */

.services-hero {
  padding-block:
    clamp(48px, 7vw, 84px);

  background:
    linear-gradient(
      165deg,
      var(--teal),
      var(--teal-deep)
    );

  color: white;
}


.eyebrow {
  display: inline-flex;

  align-items: center;

  gap: 9px;

  color: #BFE0DF;

  font-family: var(--display);

  font-stretch: 112%;

  font-weight: 700;

  font-size: 12.5px;

  letter-spacing: 0.16em;

  text-transform: uppercase;
}


.eyebrow::before {
  content: "";

  width: 26px;
  height: 2px;

  background: var(--amber);

  border-radius: 2px;
}


.services-hero h1 {
  margin-top: 14px;

  color: white;

  font-family: var(--display);

  font-size:
    clamp(38px, 6vw, 68px);

  font-weight: 900;

  font-stretch: 118%;

  line-height: 1.03;

  letter-spacing: -0.01em;
}


.services-hero p {
  max-width: 56ch;

  margin-top: 18px;

  color: #C7E0DF;

  font-size: 19px;
}


/* =========================================
   SERVICES SECTION
========================================= */

.services-section {
  padding-block:
    clamp(58px, 8vw, 104px);

  background: var(--paper-2);
}


.service-rows {
  display: flex;

  flex-direction: column;

  gap: 22px;
}


/* =========================================
   SERVICE ROW
========================================= */

.service-row {
  display: grid;

  grid-template-columns:
    1.15fr 1fr;

  overflow: hidden;

  background: white;

  border:
    1px solid var(--line);

  border-radius: 20px;
}


/*
  Alternating layout:

  1 text | image
  2 image | text
  3 text | image
*/
.service-row:nth-child(even) {
  grid-template-columns:
    1fr 1.15fr;
}


.service-row:nth-child(even)
.service-media {
  order: -1;
}


/* =========================================
   SERVICE CONTENT
========================================= */

.service-body {
  display: flex;

  flex-direction: column;

  justify-content: center;

  padding:
    clamp(26px, 3.4vw, 44px);
}


.service-tag {
  display: inline-flex;

  align-items: center;

  width: fit-content;

  padding: 6px 12px;

  border-radius: 999px;

  background: var(--paper-2);

  color: var(--teal);

  font-family: var(--display);

  font-stretch: 106%;

  font-weight: 700;

  font-size: 12px;

  letter-spacing: 0.12em;

  text-transform: uppercase;
}


.service-body h3 {
  margin-top: 16px;

  font-family: var(--display);

  font-size:
    clamp(24px, 3vw, 32px);

  font-weight: 800;

  font-stretch: 118%;

  line-height: 1.03;

  letter-spacing: -0.01em;
}


.service-body > p {
  margin-top: 12px;

  color: var(--slate);

  font-size: 16px;
}


/* =========================================
   EXAMPLES
========================================= */

.service-examples {
  display: flex;

  flex-wrap: wrap;

  gap: 8px;

  margin-top: 18px;
}


.service-examples span {
  padding: 6px 13px;

  border:
    1px solid var(--line);

  border-radius: 999px;

  background: var(--paper);

  color: var(--ink);

  font-size: 13.5px;

  font-weight: 600;
}


/* =========================================
   BUTTON
========================================= */

.service-button {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  width: fit-content;

  margin-top: 24px;

  padding: 14px 24px;

  border-radius: 999px;

  background: var(--amber);

  color: #3A2500;

  font-family: var(--display);

  font-stretch: 108%;

  font-weight: 700;

  font-size: 15.5px;

  text-decoration: none;

  box-shadow:
    0 6px 16px
    rgba(244, 155, 28, 0.35);

  transition:
    transform 0.16s ease,
    background 0.16s ease,
    box-shadow 0.16s ease;
}


.service-button:hover {
  background: var(--amber-dark);

  transform:
    translateY(-2px);
}


/* =========================================
   IMAGE
========================================= */

.service-media {
  position: relative;

  min-height: 240px;

  overflow: hidden;

  background:
    linear-gradient(
      160deg,
      var(--teal),
      var(--teal-deep)
    );
}


.service-media img {
  position: absolute;

  inset: 0;

  display: block;

  width: 100%;
  height: 100%;

  object-fit: cover;
}


/* =========================================
   CTA
========================================= */

.services-cta {
  position: relative;

  overflow: hidden;

  padding-block:
    clamp(58px, 8vw, 104px);

  background: var(--ink);

  color: white;
}


.services-cta::before {
  content: "";

  position: absolute;

  top: -60px;
  right: -60px;

  width: 340px;
  height: 340px;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(244, 155, 28, 0.20),
      transparent 68%
    );
}


.cta-inner {
  position: relative;

  display: flex;

  align-items: center;

  justify-content: space-between;

  flex-wrap: wrap;

  gap: 36px;
}


.cta-inner h2 {
  max-width: 16ch;

  color: white;

  font-family: var(--display);

  font-size:
    clamp(28px, 4vw, 44px);

  font-weight: 900;
}


.cta-actions {
  display: flex;

  flex-wrap: wrap;

  gap: 14px;
}


.cta-button {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  padding: 17px 30px;

  border:
    2px solid transparent;

  border-radius: 999px;

  font-family: var(--display);

  font-stretch: 108%;

  font-weight: 700;

  font-size: 16.5px;

  text-decoration: none;

  transition:
    transform 0.16s,
    background 0.16s,
    border-color 0.16s;
}


.cta-button.primary {
  background: var(--amber);

  color: #3A2500;

  box-shadow:
    0 6px 16px
    rgba(244, 155, 28, 0.35);
}


.cta-button.primary:hover {
  background: var(--amber-dark);

  transform:
    translateY(-2px);
}


.cta-button.outline {
  border-color:
    rgba(255, 255, 255, 0.28);

  background:
    rgba(255, 255, 255, 0.10);

  color: white;
}


.cta-button.outline:hover {
  background:
    rgba(255, 255, 255, 0.18);

  transform:
    translateY(-2px);
}


/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 960px) {

  .service-row,
  .service-row:nth-child(even) {
    grid-template-columns:
      1fr;
  }


  .service-row:nth-child(even)
  .service-media {
    order: 0;
  }


  .service-media {
    min-height: 280px;
  }


  .cta-inner {
    flex-direction: column;

    align-items: flex-start;
  }

}


@media (max-width: 600px) {

  .services-hero p {
    font-size: 17px;
  }


  .service-body {
    padding: 24px;
  }


  .service-media {
    min-height: 220px;
  }


  .service-button,
  .cta-button {
    width: 100%;
  }


  .cta-actions {
    width: 100%;
  }

}
</style>