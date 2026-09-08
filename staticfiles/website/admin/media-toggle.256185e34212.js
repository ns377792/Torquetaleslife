(function () {
  "use strict";

  const mediaSlots = [
    { type: "media_type", image: "image", video: "video" },
    { type: "media_type", image: "banner_image", video: "video" },
    { type: "banner_media_type", image: "banner_image", video: "banner_video" },
    {
      type: "background_media_type",
      image: "background_image",
      video: "background_video",
    },
  ];

  function fieldRow(fieldName) {
    return document.querySelector(`.form-row.field-${fieldName}`);
  }

  function selectedType(fieldName) {
    const checkedRadio = document.querySelector(
      `input[name="${fieldName}"]:checked`
    );
    if (checkedRadio) return checkedRadio.value;

    const select = document.querySelector(`[name="${fieldName}"]`);
    return select ? select.value : null;
  }

  function updateSlot(slot) {
    const typeInputs = document.querySelectorAll(`[name="${slot.type}"]`);
    const imageRow = fieldRow(slot.image);
    const videoRow = fieldRow(slot.video);

    if (!typeInputs.length || !imageRow || !videoRow) return;

    const showVideo = selectedType(slot.type) === "video";
    imageRow.hidden = showVideo;
    videoRow.hidden = !showVideo;

    const imageInput = imageRow.querySelector('input[type="file"]');
    const videoInput = videoRow.querySelector('input[type="file"]');
    if (imageInput) imageInput.accept = "image/*";
    if (videoInput) videoInput.accept = "video/mp4,video/webm,video/ogg";
  }

  document.addEventListener("DOMContentLoaded", function () {
    mediaSlots.forEach(function (slot) {
      const inputs = document.querySelectorAll(`[name="${slot.type}"]`);
      if (!inputs.length) return;

      inputs.forEach(function (input) {
        input.addEventListener("change", function () {
          updateSlot(slot);
        });
      });
      updateSlot(slot);
    });
  });
})();
