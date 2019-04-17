using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BrickChanger : MonoBehaviour
{
    public GameObject[] bricks;
    public Material[] materials;

    private Renderer[] childMaterials;

    Material opaque, transparent;

    // Start is called before the first frame update
    void Start()
    {
        opaque = materials[0];
        transparent = materials[1];

        ChangeMaterial(0, "opaque");
    }

    public void ChangeMaterial(int brickToChange, string material)
    {
        if(material == "transparent")
        {
            childMaterials = bricks[brickToChange].GetComponentsInChildren<MeshRenderer>();
            foreach (Renderer rend in childMaterials)
            {
                rend.material = transparent;
            }
        }
        else if(material == "opaque")
        {
            childMaterials = bricks[brickToChange].GetComponentsInChildren<MeshRenderer>();
            foreach (Renderer rend in childMaterials)
            {
                rend.material = opaque;
            }
        }

    }
}
