import { TABS } from 'react-filerobot-image-editor'

export default function ({ photo, onClose, onSave, onDisplay, onDelete }) {
  return {
    source: photo.src,
    tabsIds: [TABS.ADJUST, TABS.FINETUNE, TABS.FILTERS, TABS.ANNOTATE],
    defaultTabId: TABS.ADJUST,
    onBeforeSave: () => false,
    onSave: (args) => {
      onSave(args)
        .then(onDisplay)
        .then(onClose)
    },
    Crop: {
      autoResize: true,
      presetsItems: [{
        titleKey: 'original',
        ratio: 'original'
      },
      {
        titleKey: 'custom',
        ratio: 'custom'
      },
      {
        titleKey: 'landscape',
        descriptionKey: '5:3',
        ratio: 5 / 3
      },
      {
        titleKey: 'portrait',
        descriptionKey: '3:5',
        ratio: 3 / 5
      }]
    },
    translations: {
      save: 'Save & Display'
    },
    moreSaveOptions: [
      {
        label: 'Save',
        onClick: (args) => {
          onSave(args)
            .then(onClose)
        }
      },
      {
        label: 'Delete',
        onClick: (args) => {
          onDelete(args)
          onClose()
        }

      }
    ]
  }
}