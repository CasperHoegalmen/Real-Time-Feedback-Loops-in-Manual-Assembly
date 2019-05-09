using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class BrickChanger : MonoBehaviour
{
    public GameObject[] bricks;

    [SerializeField] Material opaque;
    [SerializeField] Material transparent;
    [SerializeField] Camera camera;
    [SerializeField] TextMeshProUGUI stepText;

    private Renderer[] childMaterials;

    Color colorOfBrick;
    CameraMovement cameraMovement;

    int currentStep = 1;

    // Start is called before the first frame update
    void Start()
    {
        cameraMovement = camera.GetComponent<CameraMovement>();
        stepText.text = "Step " + currentStep + " of " + bricks.Length;
    }

    public void ChangeMaterial(int brickToChange, string material)
    {
        colorOfBrick = bricks[brickToChange].GetComponent<Renderer>().material.color;

        if(material == "transparent")
        {
            childMaterials = bricks[brickToChange].GetComponentsInChildren<MeshRenderer>();
            foreach (Renderer rend in childMaterials)
            {
                rend.material = transparent;
                rend.material.color = new Color(colorOfBrick.r, colorOfBrick.g, colorOfBrick.b, transparent.color.a);
            }
        }
        else if(material == "opaque")
        {
            childMaterials = bricks[brickToChange].GetComponentsInChildren<MeshRenderer>();
            foreach (Renderer rend in childMaterials)
            {
                rend.material = opaque;
                rend.material.color = rend.material.color = new Color(colorOfBrick.r, colorOfBrick.g, colorOfBrick.b, opaque.color.a);
            }
        }
    }

    public void EnableBrick(int brickToEnable)
    {
        currentStep++;
        if(brickToEnable >= bricks.Length)
        {
            brickToEnable -= 1;
        }

        bricks[brickToEnable].SetActive(true);
        stepText.text = "Step " + currentStep + " of " + bricks.Length;
        cameraMovement.target = bricks[brickToEnable].transform;
    }
}
