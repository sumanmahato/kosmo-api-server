const dateFilterTypes = [
  {
    condition: "BETWEEN",
    data: "984335400000_1746729000000",
  },
  { condition: "AFTER", date: 983125800000 },
  { condition: "BEFORE", date: 983125800000 },
];

const fileSizeFilterTypes = [
  { condition: "LESS_THAN", data: "200K" },
  { condition: "BETWEEN", data: "5M_10M" },
  { condition: "IS", data: "1G" },
  { condition: "GREATER_THAN_EQUAL", data: "1024B" },
  { condition: "GREATER_THAN", data: "512M" },
];

const stringPatternFilterTypes = [
  { condition: "STARTS_WITH", data: "abc" },
  { condition: "CONTAINS", data: "xyz" },
  { condition: "IS", data: "xyz" },
  { condition: "ENDS_WITH", data: "xyz" },
];

const filterEnums = [
  "DIRECTORY_NAME",
  "FILE_NAME",
  "FILE_LAST_MODIFIED",
  "FILE_LAST_ACCESSED",
  "FILE_MOVED",
  "FILE_CATEGORY",
  "FILE_EXTENSION",
  "FILE_SIZE",
  "FILE_GROUP",
  "FILE_OWNER",
  "TAGS",
];

const filetypes = [
  "Archive",
  "Audio",
  "Binary",
  "Database",
  "DiskImage",
  "Document",
  "Image",
  "Log",
  "Mail",
  "Presentation",
  "Script",
  "SourceCode",
  "Spreadsheet",
  "Text",
  "Video",
  "VirtualMachine",
  "Other",
];

const filterTags = [
  {
    condition: null,
    tags: [
      {
        label: "politician", // key
        values: [
          { id: 1, label: "Modi" },
          { id: 2, label: "Trump" },
        ],
      },
    ],
  },
];

const schema = {
  lastModified: [], // date filter (only single value)
  lastAccessed: [], // date filter
  moved: [], // date filter
  selectedFileTypes: [], // list of file types
  fileExtensions: [".txt", ".png", ".pdf"],
  fileSizes: [], // file size filter (only single value)
  fileGroups: [], // string pattern filter (can have multiple values),
  fileOwners: [], // string pattern filter,
  directoryName: [], // string pattern filter
  filterTags,
  exclusions: [], // list of filter enums
};
