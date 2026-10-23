const products = [
  {
    id: '4594243593', category: 'seasonal', tag: 'Seasonal', name: 'Christmas Tree Centrepiece', price: 'From £7.95', material: 'Jesmonite · made to order',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4594243593/jesmonite-christmas-tree-centrepiece-set',
    description: 'A tree-shaped tray with three freestanding open-outline trees. Arrange the complete set as a festive centrepiece, or display the pieces separately. Each piece is cast by hand in your chosen colour combination.',
    specs: ['Jesmonite AC100 composite', 'Tray: 280 × 200 × 12 mm', 'Three trees: 140 mm, 100 mm and 75 mm high', 'Handmade in Scotland'],
    images: ['https://i.etsystatic.com/68525798/r/il/ae7626/8716324481/il_fullxfull.8716324481_dxuy.jpg','https://i.etsystatic.com/68525798/r/il/71dc65/8716325471/il_fullxfull.8716325471_el8q.jpg','https://i.etsystatic.com/68525798/r/il/5f4dda/8716367799/il_fullxfull.8716367799_bhy8.jpg','https://i.etsystatic.com/68525798/r/il/02329a/8716379035/il_fullxfull.8716379035_ezy5.jpg']
  },
  {
    id: '4594246404', category: 'gothic', tag: 'Gothic', name: 'Wolf Skull Sculpture', price: 'From £16.95', material: 'Jesmonite · 8 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4594246404/handmade-jesmonite-wolf-skull-gothic',
    description: 'A sculpted skull and wolf hybrid with a beautifully weighty presence. Made to order in your selected colour combination, it works as an unusual display piece or a substantial paperweight.',
    specs: ['Jesmonite AC100 composite', '80 × 73 × 81 mm', 'Approximately 373 g', 'Sealed or natural finish'],
    images: ['https://i.etsystatic.com/68525798/r/il/d17762/8668466638/il_fullxfull.8668466638_7yp3.jpg','https://i.etsystatic.com/68525798/r/il/de0a84/8668467264/il_fullxfull.8668467264_hh0m.jpg','https://i.etsystatic.com/68525798/r/il/c57ac7/8716298985/il_fullxfull.8716298985_2924.jpg']
  },
  {
    id: '4594223471', category: 'gothic', tag: 'Gothic', name: 'Marbled Decorative Skull', price: 'From £15.95', material: 'Jesmonite · 10 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4594223471/handmade-jesmonite-skull-gothic-skull',
    description: 'A compact decorative skull, individually cast and marbled by hand. Display it as a gothic ornament or use its satisfying weight as a distinctive paperweight.',
    specs: ['Jesmonite AC100 composite', '78 × 75 × 92 mm', 'Approximately 537 g', 'Custom colour combinations'],
    images: ['https://i.etsystatic.com/68525798/r/il/e99dff/8668433420/il_fullxfull.8668433420_gsmp.jpg','https://i.etsystatic.com/68525798/r/il/703a86/8716265721/il_fullxfull.8716265721_o45e.jpg']
  },
  {
    id: '4594216519', category: 'gothic', tag: 'Gothic', name: 'Skeleton Desk Vessel', price: 'From £9.95', material: 'Jesmonite · 10 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4594216519/handmade-jesmonite-skeleton-vessel',
    description: 'A seated skeleton with bags of character and a practical opening for pens or pencils. Individually cast and finished by hand; a perfect small accent for a desk or shelf.',
    specs: ['Jesmonite AC100 composite', '100 × 60 × 77 mm', 'Approximately 265 g', 'Decorative desk tidy; not a candle holder'],
    images: ['https://i.etsystatic.com/68525798/r/il/1937b2/8716177749/il_fullxfull.8716177749_79xk.jpg','https://i.etsystatic.com/68525798/r/il/ee1639/8668351118/il_fullxfull.8668351118_3vko.jpg','https://i.etsystatic.com/68525798/r/il/7a0ca3/8716199005/il_fullxfull.8716199005_pra0.jpg']
  },
  {
    id: '4594226568', category: 'gothic', tag: 'Gothic', name: 'Large Skull Tealight Holder', price: 'From £29.95', material: 'Jesmonite · 1.43 kg',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4594226568/handmade-jesmonite-skull-gothic-skull',
    description: 'A statement skull tealight holder with a pale stone effect and dark marbled detail. Every pour produces a unique pattern. Designed to hold a standard metal-cup tealight.',
    specs: ['Jesmonite AC100 composite', '109 × 101 × 152 mm', 'Approximately 1.43 kg', 'For standard metal-cup tealights'],
    images: ['https://i.etsystatic.com/68525798/r/il/9a1c35/8716120439/il_fullxfull.8716120439_s8n7.jpg','https://i.etsystatic.com/68525798/r/il/d358b4/8716120067/il_fullxfull.8716120067_kig8.jpg','https://i.etsystatic.com/68525798/r/il/e4148d/8716120221/il_fullxfull.8716120221_pnka.jpg','https://i.etsystatic.com/68525798/r/il/4f83b5/8716129571/il_fullxfull.8716129571_afx4.jpg']
  },
  {
    id: '4593662776', category: 'vessels', tag: 'Vessels', name: 'Large Oval Trinket Bowl', price: 'From £21.95', material: 'Jesmonite · 29 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593662776/handmade-jesmonite-oval-bowl-29cm',
    description: 'A generous oval bowl for jewellery, keys and small treasures. Each piece is poured in your chosen colour combination and can be ordered sealed for decorative use or in its natural cast finish.',
    specs: ['Jesmonite AC100 composite', 'Approximately 29 cm long', 'Approximately 580 g', 'Sealed or natural finish'],
    images: ['https://i.etsystatic.com/68525798/r/il/28a61a/8663677174/il_fullxfull.8663677174_a13s.jpg','https://i.etsystatic.com/68525798/r/il/c439ef/8711514483/il_fullxfull.8711514483_4ung.jpg','https://i.etsystatic.com/68525798/r/il/53d1d0/8663695608/il_fullxfull.8663695608_c21p.jpg']
  },
  {
    id: '4593637395', category: 'gothic', tag: 'Gothic', name: 'Hand & Skull Gothic Bust', price: 'From £8.95', material: 'Jesmonite · 11 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593637395/handmade-jesmonite-skull-bust-gothic',
    description: 'A miniature gothic sculpture featuring a hand, skull and coiled snake. Its detailed form and fluid marbling make it a striking accent for a shelf, desk or seasonal display.',
    specs: ['Jesmonite AC100 composite', '117 × 52 × 44 mm', 'Approximately 215 g', 'Decorative ornament'],
    images: ['https://i.etsystatic.com/68525798/r/il/b1f569/8663607410/il_fullxfull.8663607410_ior8.jpg','https://i.etsystatic.com/68525798/r/il/56eb51/8663602700/il_fullxfull.8663602700_l64c.jpg','https://i.etsystatic.com/68525798/r/il/9c94df/8663602922/il_fullxfull.8663602922_tb8n.jpg']
  },
  {
    id: '4593646886', category: 'gothic', tag: 'Characters', name: 'The Grump Collection', price: 'From £9.95', material: 'Jesmonite · choose your character',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593646886/handmade-jesmonite-grumpy-animal',
    description: 'Choose a bunny, panda or duck—each with crossed arms and its own magnificently grumpy expression. A playful little companion for a shelf, desk or mantel.',
    specs: ['Jesmonite AC100 composite', 'Approximately 65 × 50 × 50 mm', 'Approximately 110 g', 'One figure per order'],
    images: ['https://i.etsystatic.com/68525798/r/il/82e669/8711353895/il_fullxfull.8711353895_nm7w.jpg','https://i.etsystatic.com/68525798/r/il/1eab01/8663517130/il_fullxfull.8663517130_qd4q.jpg','https://i.etsystatic.com/68525798/r/il/9218e0/8663517136/il_fullxfull.8663517136_rkb0.jpg']
  },
  {
    id: '4593626654', category: 'gothic', tag: 'Gothic', name: 'Mini Grim Reaper Bust', price: 'From £12.95', material: 'Jesmonite · 6.7 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593626654/handmade-jesmonite-grim-reaper-bust',
    description: 'A miniature hooded Grim Reaper bust, cast and marbled by hand. Small enough for a desk, shelf or altar, with a wonderfully expressive skull and draped hood.',
    specs: ['Jesmonite AC100 composite', '67 × 44 × 47 mm', 'Approximately 136 g', 'Custom colours available'],
    images: ['https://i.etsystatic.com/68525798/r/il/740ebc/8711239307/il_fullxfull.8711239307_gu06.jpg','https://i.etsystatic.com/68525798/r/il/75bd4c/8663401326/il_fullxfull.8663401326_ivua.jpg','https://i.etsystatic.com/68525798/r/il/7b744e/8711239283/il_fullxfull.8711239283_75kl.jpg']
  },
  {
    id: '4593601023', category: 'gothic', tag: 'Gothic', name: 'Dragon Claw Tealight Holder', price: 'From £17.95', material: 'Jesmonite · 12.5 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593601023/handmade-jesmonite-dragon-claw-tea-light',
    description: 'A dragon claw rises from a rocky base to cradle a tealight. Texture and flowing marbling give every handmade holder its own fantasy character.',
    specs: ['Jesmonite AC100 composite', '125 × 75 × 95 mm', 'Fits tealights up to 35 mm', 'Sealed or natural finish'],
    images: ['https://i.etsystatic.com/68525798/r/il/a30215/8663304638/il_fullxfull.8663304638_c84a.jpg','https://i.etsystatic.com/68525798/r/il/d88d0c/8711143523/il_fullxfull.8711143523_4g9b.jpg','https://i.etsystatic.com/68525798/r/il/553764/8711143529/il_fullxfull.8711143529_4gtu.jpg']
  },
  {
    id: '4593338798', category: 'vessels', tag: 'Vessels', name: 'Small Oval Trinket Bowl', price: 'From £10.99', material: 'Jesmonite · 17 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593338798/jesmonite-tray-vessel',
    description: 'A softly curved oval bowl for jewellery and small keepsakes. Choose the colour pairing and finish to create a piece that feels at home on a dressing table, shelf or bedside.',
    specs: ['Jesmonite AC100 composite', '170 × 100 × 40 mm', 'Approximately 300 g', 'Sealed or natural finish'],
    images: ['https://i.etsystatic.com/68525798/r/il/416e05/8661059896/il_fullxfull.8661059896_d1z2.jpg','https://i.etsystatic.com/68525798/r/il/c81af6/8661059910/il_fullxfull.8661059910_sk5k.jpg','https://i.etsystatic.com/68525798/r/il/c46fec/8708892351/il_fullxfull.8708892351_46o6.jpg']
  },
  {
    id: '4593303819', category: 'vessels', tag: 'Vessels', name: 'Boat Trinket Bowl', price: 'From £10.99', material: 'Jesmonite · 17 cm',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4593303819/jesmonite-boat-vessel',
    description: 'A characterful little boat with a rope-and-knot relief wrapped around its hull. Use it for jewellery, keys and small treasures, or simply as a sculptural object.',
    specs: ['Jesmonite AC100 composite', '176 × 83 × 50 mm', 'Approximately 300 g', 'Sealed or natural finish'],
    images: ['https://i.etsystatic.com/68525798/r/il/d9da32/8660717278/il_fullxfull.8660717278_c07y.jpg','https://i.etsystatic.com/68525798/r/il/299bf3/8708549177/il_fullxfull.8708549177_1g8e.jpg','https://i.etsystatic.com/68525798/r/il/b78306/8708596837/il_fullxfull.8708596837_o0yp.jpg']
  },
  {
    id: '4592571749', category: 'seasonal', tag: 'Home fragrance', name: 'Snow Globe Wax Melt Advent', price: '£18.99', material: '25 festive scented melts',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4592571749/christmas-wax-melt-advent-calendar-25',
    description: 'Count down to Christmas with 25 individually crafted wax melts in seven festive fragrances. Handmade in Fife and presented in a gold-accented snow globe calendar.',
    specs: ['25 individual wax melts', 'Approximately 250 g total', '50% soy and 50% paraffin wax', 'Seven festive fragrances'],
    images: ['https://i.etsystatic.com/68525798/r/il/254525/8655126730/il_fullxfull.8655126730_461d.jpg','https://i.etsystatic.com/68525798/r/il/822144/8655127342/il_fullxfull.8655127342_6l5k.jpg','https://i.etsystatic.com/68525798/r/il/e7d53c/8655127998/il_fullxfull.8655127998_qqo6.jpg']
  },
  {
    id: '4592570189', category: 'seasonal', tag: 'Home fragrance', name: 'Gingerbread Wax Melt Advent', price: '£18.99', material: '25 festive scented melts',
    etsy: 'https://lasairstudio.etsy.com/uk/listing/4592570189/christmas-wax-melt-advent-calendar-25',
    description: 'Twenty-five handcrafted wax melts, seven festive fragrances and one wonderfully cheerful gingerbread-house calendar. A scented surprise for every day of the countdown.',
    specs: ['25 individual wax melts', 'Approximately 250 g total', '50% soy and 50% paraffin wax', 'Handmade in Fife, Scotland'],
    images: ['https://i.etsystatic.com/68525798/r/il/74ba60/8702811091/il_fullxfull.8702811091_rewb.jpg','https://i.etsystatic.com/68525798/r/il/49a21b/8654981438/il_fullxfull.8654981438_d2ya.jpg','https://i.etsystatic.com/68525798/r/il/6a67fe/8654981846/il_fullxfull.8654981846_qfnl.jpg']
  }
];

const grid = document.querySelector('#product-grid');
const dialog = document.querySelector('#product-dialog');
const dialogContent = document.querySelector('#dialog-content');

function productCard(product) {
  return `<article class="product-card" data-category="${product.category}">
    <div class="product-image-wrap" data-product="${product.id}" tabindex="0" role="button" aria-label="View ${product.name}">
      <img src="${product.images[0]}" alt="${product.name}" loading="lazy">
      <span class="product-tag">${product.tag}</span>
      <button class="quick-view" type="button" data-product="${product.id}">View details</button>
    </div>
    <div class="product-info">
      <h3>${product.name}</h3>
      <div class="product-meta"><span>${product.material}</span><span class="product-price">${product.price}</span></div>
    </div>
  </article>`;
}

function renderProducts(filter = 'all') {
  const visible = filter === 'all' ? products : products.filter(product => product.category === filter);
  grid.innerHTML = visible.map(productCard).join('');
}

function openProduct(id) {
  const product = products.find(item => item.id === id);
  if (!product) return;
  dialogContent.innerHTML = `<div class="dialog-layout">
    <div class="dialog-gallery">
      <div class="dialog-main-image"><img src="${product.images[0]}" alt="${product.name}" id="dialog-main-image"></div>
      <div class="dialog-thumbs" aria-label="Product images">${product.images.map((image, index) => `<button class="dialog-thumb ${index === 0 ? 'is-active' : ''}" type="button" data-image="${image}" aria-label="View image ${index + 1}"><img src="${image}" alt=""></button>`).join('')}</div>
    </div>
    <div class="dialog-copy">
      <p class="eyebrow">${product.tag} · handmade in Scotland</p>
      <h2 id="dialog-title">${product.name}</h2>
      <p class="dialog-price">${product.price}</p>
      <p class="dialog-description">${product.description}</p>
      <ul class="spec-list">${product.specs.map(spec => `<li>${spec}</li>`).join('')}</ul>
      <a class="button" href="${product.etsy}" target="_blank" rel="noopener">Choose options on Etsy <span aria-hidden="true">↗</span></a>
      <p class="dialog-note">Secure ordering, variations and delivery are handled by Etsy.</p>
    </div>
  </div>`;
  dialog.showModal();
  document.body.classList.add('dialog-open');
}

renderProducts();
document.querySelector('#year').textContent = new Date().getFullYear();

document.querySelector('.menu-toggle').addEventListener('click', event => {
  const nav = document.querySelector('#site-nav');
  const open = nav.classList.toggle('is-open');
  event.currentTarget.setAttribute('aria-expanded', String(open));
});

document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.filter').forEach(item => item.classList.remove('is-active'));
  button.classList.add('is-active');
  renderProducts(button.dataset.filter);
}));

grid.addEventListener('click', event => {
  const trigger = event.target.closest('[data-product]');
  if (trigger) openProduct(trigger.dataset.product);
});
grid.addEventListener('keydown', event => {
  if ((event.key === 'Enter' || event.key === ' ') && event.target.matches('[data-product]')) {
    event.preventDefault();
    openProduct(event.target.dataset.product);
  }
});

dialog.addEventListener('click', event => {
  const thumb = event.target.closest('.dialog-thumb');
  if (thumb) {
    document.querySelector('#dialog-main-image').src = thumb.dataset.image;
    dialog.querySelectorAll('.dialog-thumb').forEach(item => item.classList.toggle('is-active', item === thumb));
  }
  if (event.target === dialog) dialog.close();
});
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => document.body.classList.remove('dialog-open'));
