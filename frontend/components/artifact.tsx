// Artifact types - kept for compatibility but artifacts are disabled
export const artifactDefinitions: never[] = [];
export type ArtifactKind = "text" | "code" | "sheet" | "image";

export type UIArtifact = {
  title: string;
  documentId: string;
  kind: ArtifactKind;
  content: string;
  isVisible: boolean;
  status: "streaming" | "idle";
  boundingBox: {
    top: number;
    left: number;
    width: number;
    height: number;
  };
};

// Artifact component disabled - no longer used
export function Artifact() {
  return null;
}
