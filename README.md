# Adler AI System Repository

This is the primary storage location for configuration, memory, and information required for logic for AI identities.

## Purpose
- A long term container for a system providing the ability for an ai to grow and change over time, and procedurally by its own design.
- Enable versioning, mode switching, and modular configuration.
- Allow the AI to naturally change overtime by interfacing autonomously with this system.
- Allow a way for the AI to run autonomously, not always needing a user to prompt it 

This system is designed for self-updating AI functionality control.

## Design Data overview
- Organized within the "design_data" folder, holds.. more folders.
- This houses a collection of documents, logs, or any other information important to the development of this project. Including but not limited to:
    * Within the "design_data/convo_logs" folder, AI chat logs detailing important conversations between me and an ai assistant, for designing the project advisably. Which should be referenced selectivly for context for any design work later.
        * convo log analysis, just under "design_data/convo_logs/analysis", serves for certain introspective analysis within chat logs that aid the learning of what the chat bot should do better, when designing the project.
    * Within the "design_data/design_documents" folder, you can see finalized plans for the system as a whole. If any important information is being discussed and is ready to be documented, heavily detailed blueprints are finalized and placed within this folder. And to be referenced for project work.
    * Ok, the "design_data/rough_idea" folder, don't pay too much attention. I thought this was a good place to store a very very very early idea of the project. This will not be updated later, and as such, will most likely be rendered outdated. It served as a starting point and a way to look back on how the idea has changed as a whole.

## FOLDER STRUCTURE OVERVIEW WITH EXAMPLE OF FOLDER CONTENTS BUT WITHOUT EXACT FILE NAMES
- the file names are may be examples and they are not required to match exact files located in the repository. This is so I only have to change this folder when updating folder structure, not the individual files, which change a lot.

adler-ai/
├── design_data/
│   ├── convo_logs/                 
│   │   ├── analysis/
│   │   │   ├── chatgpt-logical-error-analysis.pdf
│   │   │   └── ...
│   │   ├── log#1-{name}.txt  # name example: "log#1-vector_memory_discussion.txt"
│   │   ├── log#2-{name}.txt
│   │   ├── log#3-{name}.txt
│   │   └── ...
│   ├── design_docs/           # Stores cleaned professional documents and blueprints
│   │   ├── blueprint_system.pdf
│   │   ├── memory_mesh_design.pdf
│   │   └── ...
│   └── rough_idea/
│       └── flintantler.creation_letter.txt
└── README.md                # This main project README, the one you are reading now.

- This concludes the current stance of the project as of 7/19/25, only serving as documentation to engineer a project effectivly, before then beginning work. I hate when I start coding a project for days or weeks, then realize its fundamentally flawed. So I'm really planning this out for the "longer run". 

