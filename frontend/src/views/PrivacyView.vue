<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n({
  useScope: 'global',
})
</script>

<template>
  <main class="privacy-page">

    <!-- HERO -->
    <section class="privacy-hero">

      <div class="privacy-wrap">

        <span class="eyebrow">
          {{ t('privacyPage.hero.eyebrow') }}
        </span>

        <h1>
          {{ t('privacyPage.hero.title') }}
        </h1>

        <p>
          {{ t('privacyPage.hero.description') }}
        </p>

      </div>

    </section>


    <!-- CONTENT -->
    <section class="privacy-section">

      <div class="privacy-wrap">

        <div class="privacy-layout">

          <div class="privacy-content">


            <!-- 1 -->
            <section class="privacy-card">

              <span class="section-number">
                1
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.controller.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.controller.description') }}
                </p>

                <div class="company-box">

                  <strong>
                    NOVARI GbR
                  </strong>

                  <span>
                    {{ t('privacyPage.controller.addressPlaceholder') }}
                  </span>

                  <span>
                    Koblenz, Germany
                  </span>

                  <span>
                    {{ t('privacyPage.controller.email') }}:
                    <a href="mailto:Novari2026@yahoo.com">
                      Novari2026@yahoo.com
                    </a>
                  </span>

                  <span>
                    {{ t('privacyPage.controller.phone') }}:
                    <a href="tel:+491739523061">
                      0173 9523061
                    </a>
                  </span>

                </div>

              </div>

            </section>


            <!-- 2 -->
            <section class="privacy-card">

              <span class="section-number">
                2
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.general.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.general.text1') }}
                </p>

                <p>
                  {{ t('privacyPage.general.text2') }}
                </p>

              </div>

            </section>


            <!-- 3 -->
            <section class="privacy-card">

              <span class="section-number">
                3
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.hosting.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.hosting.text1') }}
                </p>

                <p>
                  {{ t('privacyPage.hosting.text2') }}
                </p>

                <div class="notice-box">
                  {{ t('privacyPage.hosting.notice') }}
                </div>

              </div>

            </section>


            <!-- 4 -->
            <section class="privacy-card">

              <span class="section-number">
                4
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.contact.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.contact.text1') }}
                </p>

                <p>
                  {{ t('privacyPage.contact.text2') }}
                </p>

              </div>

            </section>


            <!-- 5 -->
            <section class="privacy-card">

              <span class="section-number">
                5
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.forms.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.forms.text1') }}
                </p>

                <p>
                  {{ t('privacyPage.forms.text2') }}
                </p>

                <p>
                  {{ t('privacyPage.forms.text3') }}
                </p>

              </div>

            </section>


            <!-- 6 -->
            <section class="privacy-card">

              <span class="section-number">
                6
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.uploads.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.uploads.text') }}
                </p>

              </div>

            </section>


            <!-- 7 -->
            <section class="privacy-card">

              <span class="section-number">
                7
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.whatsapp.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.whatsapp.text') }}
                </p>

              </div>

            </section>


            <!-- 8 -->
            <section class="privacy-card">

              <span class="section-number">
                8
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.maps.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.maps.text') }}
                </p>

              </div>

            </section>


            <!-- 9 -->
            <section class="privacy-card">

              <span class="section-number">
                9
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.fonts.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.fonts.text') }}
                </p>

              </div>

            </section>


            <!-- 10 -->
            <section class="privacy-card">

              <span class="section-number">
                10
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.storage.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.storage.text') }}
                </p>

              </div>

            </section>


            <!-- 11 -->
            <section class="privacy-card">

              <span class="section-number">
                11
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.rights.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.rights.intro') }}
                </p>

                <ul>
                  <li>
                    {{ t('privacyPage.rights.access') }}
                  </li>

                  <li>
                    {{ t('privacyPage.rights.rectification') }}
                  </li>

                  <li>
                    {{ t('privacyPage.rights.erasure') }}
                  </li>

                  <li>
                    {{ t('privacyPage.rights.restriction') }}
                  </li>

                  <li>
                    {{ t('privacyPage.rights.portability') }}
                  </li>

                  <li>
                    {{ t('privacyPage.rights.objection') }}
                  </li>

                  <li>
                    {{ t('privacyPage.rights.withdrawal') }}
                  </li>
                </ul>

              </div>

            </section>


            <!-- 12 -->
            <section class="privacy-card">

              <span class="section-number">
                12
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.complaint.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.complaint.text') }}
                </p>

              </div>

            </section>


            <!-- 13 -->
            <section class="privacy-card">

              <span class="section-number">
                13
              </span>

              <div>

                <h2>
                  {{ t('privacyPage.changes.title') }}
                </h2>

                <p>
                  {{ t('privacyPage.changes.text') }}
                </p>

                <p class="last-updated">
                  {{ t('privacyPage.changes.updated') }}
                </p>

              </div>

            </section>

          </div>


          <!-- SIDE CARD -->
          <aside class="privacy-aside">

            <h3>
              {{ t('privacyPage.aside.title') }}
            </h3>

            <p>
              {{ t('privacyPage.aside.description') }}
            </p>

            <div class="aside-contact">

              <a href="mailto:Novari2026@yahoo.com">

                <small>
                  {{ t('privacyPage.aside.email') }}
                </small>

                <strong>
                  Novari2026@yahoo.com
                </strong>

              </a>


              <a href="tel:+491739523061">

                <small>
                  {{ t('privacyPage.aside.phone') }}
                </small>

                <strong>
                  0173 9523061
                </strong>

              </a>

            </div>

          </aside>

        </div>

      </div>

    </section>

  </main>
</template>


<style scoped>
.privacy-page {
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
}


.privacy-wrap {
  width: 100%;
  max-width: 1180px;
  margin-inline: auto;
  padding-inline: clamp(18px, 4vw, 32px);
}


/* HERO */

.privacy-hero {
  padding-block: clamp(48px, 7vw, 84px);

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
  font-weight: 700;
  font-size: 12.5px;

  letter-spacing: 0.16em;
  text-transform: uppercase;
}


.eyebrow::before {
  content: "";

  width: 26px;
  height: 2px;

  border-radius: 2px;

  background: var(--amber);
}


.privacy-hero h1 {
  margin-top: 14px;

  color: white;

  font-family: var(--display);

  font-size:
    clamp(38px, 6vw, 68px);

  font-weight: 900;

  line-height: 1.03;
}


.privacy-hero p {
  max-width: 58ch;

  margin-top: 18px;

  color: #C7E0DF;

  font-size: 19px;
}


/* SECTION */

.privacy-section {
  padding-block:
    clamp(58px, 8vw, 104px);

  background: var(--paper-2);
}


.privacy-layout {
  display: grid;

  grid-template-columns:
    minmax(0, 1fr) 320px;

  gap:
    clamp(24px, 3.5vw, 44px);

  align-items: start;
}


.privacy-content {
  display: flex;

  flex-direction: column;

  gap: 16px;
}


/* CONTENT CARD */

.privacy-card {
  display: grid;

  grid-template-columns:
    42px minmax(0, 1fr);

  gap: 18px;

  padding:
    clamp(22px, 3vw, 32px);

  border:
    1px solid var(--line);

  border-radius: 20px;

  background: white;

  box-shadow:
    0 1px 2px rgba(12, 39, 43, 0.05);
}


.section-number {
  display: flex;

  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;

  border-radius: 9px;

  background: var(--teal);

  color: white;

  font-family: var(--display);

  font-size: 14px;

  font-weight: 800;
}


.privacy-card h2 {
  font-family: var(--display);

  font-size:
    clamp(20px, 2.4vw, 26px);

  font-weight: 800;
}


.privacy-card p {
  margin-top: 12px;

  color: var(--slate);

  font-size: 15.5px;

  line-height: 1.7;
}


.privacy-card ul {
  margin:
    16px 0 0;

  padding-inline-start: 22px;

  color: var(--slate);
}


.privacy-card li {
  margin-bottom: 8px;
}


.privacy-card a {
  color: var(--teal);

  text-decoration: underline;
}


/* COMPANY DETAILS */

.company-box {
  display: flex;

  flex-direction: column;

  gap: 4px;

  margin-top: 18px;

  padding: 18px;

  border:
    1px solid var(--line);

  border-radius: 12px;

  background: var(--paper);
}


.company-box strong {
  margin-bottom: 5px;

  color: var(--ink);

  font-family: var(--display);

  font-size: 17px;
}


/* NOTICE */

.notice-box {
  margin-top: 18px;

  padding: 15px 17px;

  border-inline-start:
    4px solid var(--amber);

  border-radius: 8px;

  background: #FFF9EF;

  color: var(--slate);

  font-size: 14px;
}


.last-updated {
  font-weight: 600;
}


/* ASIDE */

.privacy-aside {
  position: sticky;

  top: 96px;

  padding:
    clamp(24px, 3vw, 32px);

  border-radius: 20px;

  background:
    linear-gradient(
      165deg,
      var(--teal),
      var(--teal-deep)
    );

  color: white;
}


.privacy-aside h3 {
  color: white;

  font-size: 25px;

  font-weight: 800;
}


.privacy-aside > p {
  margin-top: 12px;

  color: #C7E0DF;

  font-size: 15px;
}


.aside-contact {
  display: flex;

  flex-direction: column;

  gap: 10px;

  margin-top: 24px;

  padding-top: 20px;

  border-top:
    1px solid rgba(255, 255, 255, 0.16);
}


.aside-contact a {
  display: block;

  padding: 13px 15px;

  border:
    1px solid rgba(255, 255, 255, 0.14);

  border-radius: 10px;

  background:
    rgba(255, 255, 255, 0.08);

  color: white;

  text-decoration: none;
}


.aside-contact a:hover {
  background:
    rgba(255, 255, 255, 0.16);
}


.aside-contact small {
  display: block;

  color: #A9C8C7;

  font-size: 12px;
}


.aside-contact strong {
  display: block;

  margin-top: 2px;

  overflow-wrap: anywhere;

  font-family: var(--display);

  font-size: 15px;
}


/* RESPONSIVE */

@media (max-width: 960px) {

  .privacy-layout {
    grid-template-columns:
      1fr;
  }


  .privacy-aside {
    position: static;
  }

}


@media (max-width: 600px) {

  .privacy-card {
    grid-template-columns:
      1fr;
  }


  .privacy-hero p {
    font-size: 17px;
  }

}
</style>