import { useCallback } from "react";
import {
  applyEdgeChanges,
  applyNodeChanges,
  Connection,
  EdgeAddChange,
  EdgeChange,
  EdgeRemoveChange,
  EdgeResetChange,
  getConnectedEdges,
  NodeAddChange,
  NodeChange,
  NodeResetChange,
  OnConnect,
  OnEdgesChange,
  OnNodesChange,
} from "reactflow";

import useNode from "@/hooks/useNode";
import { GraphEdge } from "@/types";

const isNodeAddChange = (change: NodeChange): change is NodeAddChange => change.type === "add";
const isNodeResetChange = (change: NodeChange): change is NodeResetChange =>
  change.type === "reset";

const isEdgeAddChange = (change: EdgeChange): change is EdgeAddChange => change.type === "add";
const isEdgeResetChange = (change: EdgeChange): change is EdgeResetChange =>
  change.type === "reset";
const isEdgeRemoveChange = (change: EdgeChange): change is EdgeRemoveChange =>
  change.type === "remove";

function useYdocState(): [OnNodesChange, OnEdgesChange, OnConnect] {
  const {
    nodesMap,
    edgesMap,
    nodesSelection,
    setNodesSelection,
    edgesSelection,
    setEdgesSelection,
  } = useNode();

  // The onNodesChange callback updates nodesMap.
  // When the changes are applied to the map, the observer will be triggered and updates the nodes state.
  const onNodesChanges: OnNodesChange = useCallback(
    (changes) => {
      const nodes = Array.from(nodesMap.values());

      const nextNodes = applyNodeChanges(changes, nodes);
      const newSelection = new Set([...nodesSelection]);
      changes.forEach((change: NodeChange) => {
        if (!isNodeAddChange(change) && !isNodeResetChange(change)) {
          const node = nextNodes.find((n) => n.id === change.id);

          if (change.type == "select") {
            if (change.selected == true) {
              newSelection.add(change.id);
            } else {
              newSelection.delete(change.id);
            }
          } else if (node && change.type !== "remove") {
            nodesMap.set(change.id, node);
          } else if (change.type === "remove") {
            const deletedNode = nodesMap.get(change.id);
            nodesMap.delete(change.id);
            // when a node is removed, we also need to remove the connected edges
            const edges = Array.from(edgesMap.values()).map((e) => e);
            const connectedEdges = getConnectedEdges(deletedNode ? [deletedNode] : [], edges);
            connectedEdges.forEach((edge) => edgesMap.delete(edge.id));
          }
        }
      });
      setNodesSelection(newSelection);
    },
    [edgesMap, nodesMap, nodesSelection],
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => {
      const currentEdges = Array.from(edgesMap.values()).filter((e) => e);
      const nextEdges = applyEdgeChanges(changes, currentEdges);
      const newSelection = new Set([...edgesSelection]);
      changes.forEach((change: EdgeChange) => {
        console.log(change);
        if (isEdgeRemoveChange(change)) {
          edgesMap.delete(change.id);
        } else if (!isEdgeAddChange(change) && !isEdgeResetChange(change)) {
          if (change.type == "select") {
            if (change.selected == true) {
              newSelection.add(change.id);
            } else {
              newSelection.delete(change.id);
            }
          } else {
            edgesMap.set(change.id, nextEdges.find((n) => n.id === change.id) as GraphEdge);
          }
        }
      });
      setEdgesSelection(newSelection);
    },
    [edgesMap, edgesSelection],
  );

  const onConnect = useCallback(
    (params: Connection | GraphEdge) => {
      const { source, sourceHandle, target, targetHandle } = params;
      const id = `edge-${source}${sourceHandle || ""}-${target}${targetHandle || ""}`;

      edgesMap.set(id, {
        id,
        ...params,
      } as GraphEdge);
    },
    [edgesMap],
  );

  return [onNodesChanges, onEdgesChange, onConnect];
}

export default useYdocState;