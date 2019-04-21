using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BrickChanger : MonoBehaviour
{
    public GameObject[] bricks;

    [SerializeField] Material opaque;
    [SerializeField] Material transparent;
    [SerializeField] Camera camera;

    private Renderer[] childMaterials;

    Color colorOfBrick;
    CameraMovement cameraMovement;

    // Start is called before the first frame update
    void Start()
    {
        cameraMovement = camera.GetComponent<CameraMovement>();
    }

    private void Update()
    {
        DoSomething("[1]", 0);
        DoSomething("[2]", 1);
        DoSomething("[3]", 2);
        DoSomething("[4]", 3);
        DoSomething("[5]", 4);
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
        if(brickToEnable >= bricks.Length)
        {
            brickToEnable -= 1;
        }

        bricks[brickToEnable].SetActive(true);
        cameraMovement.target = bricks[brickToEnable].transform;
    }

    private void DoSomething(string number, int brick)
    {
        if (Input.GetKeyDown(number))
        {
            EnableBrick(brick + 1);
            ChangeMaterial(brick, "opaque");
        }
    }
}
